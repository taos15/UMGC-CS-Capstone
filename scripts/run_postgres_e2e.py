"""Run the real browser/API/database path against a disposable *_e2e database."""
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen
from uuid import uuid4

from sqlalchemy.engine import make_url
from skillmatch.core.security import hash_password

ROOT = Path(__file__).resolve().parents[1]


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def wait_ready(url, process):
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError('Integration server exited before readiness')
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError('Integration server did not become ready')


def main():
    url = os.environ.get('SKILLMATCH_E2E_DATABASE_URL', '')
    parsed = make_url(url)
    if parsed.drivername != 'postgresql+psycopg' or not (parsed.database or '').endswith('_e2e'):
        raise SystemExit('Set SKILLMATCH_E2E_DATABASE_URL to a disposable PostgreSQL *_e2e database.')
    backend_port, frontend_port = free_port(), free_port()
    password = secrets.token_urlsafe(24)
    username = 'integration-' + secrets.token_hex(6)
    env = {**os.environ, 'DATABASE_URL': url,
        'SKILLMATCH_JWT_SECRET': secrets.token_urlsafe(48),
        'SKILLMATCH_LOCAL_USERS': json.dumps({username: {'user_id': str(uuid4()),
            'role': 'ADMIN', 'password_hash': hash_password(password)}}),
        'SKILLMATCH_API_PROXY_TARGET': f'http://127.0.0.1:{backend_port}',
        'VITE_API_BASE_URL': '/api/v1',
        'SKILLMATCH_E2E_BASE_URL': f'http://127.0.0.1:{frontend_port}',
        'SKILLMATCH_E2E_USERNAME': username, 'SKILLMATCH_E2E_PASSWORD': password}
    subprocess.run([sys.executable, '-m', 'alembic', 'upgrade', 'head'], cwd=ROOT, env=env, check=True)
    subprocess.run([sys.executable, str(ROOT/'scripts/seed_data.py')], cwd=ROOT, env=env, check=True)
    processes = []
    with tempfile.TemporaryDirectory(prefix='skillmatch-e2e-') as temporary:
        with (Path(temporary)/'servers.log').open('w') as logs:
            try:
                backend = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'skillmatch.main:app',
                    '--host', '127.0.0.1', '--port', str(backend_port)], cwd=ROOT, env=env, stdout=logs, stderr=logs)
                processes.append(backend)
                wait_ready(f'http://127.0.0.1:{backend_port}/health', backend)
                frontend = subprocess.Popen(['npm', 'run', 'dev', '--', '--host', '127.0.0.1', '--port',
                    str(frontend_port), '--strictPort'], cwd=ROOT/'frontend', env=env, stdout=logs, stderr=logs)
                processes.append(frontend)
                wait_ready(env['SKILLMATCH_E2E_BASE_URL'], frontend)
                subprocess.run(['npm', 'run', 'test:e2e'], cwd=ROOT/'frontend', env=env, check=True)
                # A new process/session confirms persistence independently of HTTP responses.
                verify = '''from sqlmodel import Session, select
from sqlalchemy import text
from skillmatch.db.session import engine
from skillmatch.features.recommendations.models import MatchRun, CandidateResult
from skillmatch.features.feedback.models import Feedback
with Session(engine) as s:
    run = s.exec(select(MatchRun).order_by(MatchRun.generated_at.desc())).first()
    assert run is not None
    candidates = list(s.exec(select(CandidateResult).where(CandidateResult.match_run_id == run.match_run_id)))
    feedback = list(s.exec(select(Feedback).where(Feedback.match_run_id == run.match_run_id)))
    assert candidates and feedback and feedback[-1].decision == 'SELECTED'
    assert feedback[-1].selected_employee_id in [c.employee_id for c in candidates if c.eligible]
    print('Independent PostgreSQL session verified run, candidates, and SELECTED feedback.')
'''
                subprocess.run([sys.executable, '-c', verify], cwd=ROOT, env=env, check=True)
            finally:
                for process in reversed(processes):
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
    print('Real React -> FastAPI -> PostgreSQL -> matcher -> stored run -> React path passed.')


if __name__ == '__main__':
    main()
