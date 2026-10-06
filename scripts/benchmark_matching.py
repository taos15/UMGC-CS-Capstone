"""Measure real HTTP recommendation latency with 100 persisted ACTIVE profiles."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import secrets
import subprocess
import sys
import tempfile
import time
from urllib.request import Request, urlopen
from uuid import uuid4, uuid5, NAMESPACE_URL

from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlmodel import Session, create_engine, select
from skillmatch.core.security import hash_password
from skillmatch.features.employees.models import EmployeeRecord
from skillmatch.features.employees.schemas import EmployeeProfile
from skillmatch.features.jobs.models import JobRecord
from skillmatch.features.jobs.schemas import JobProfile
from skillmatch.features.skills.models import SkillRecord
from run_postgres_e2e import free_port, wait_ready

ROOT = Path(__file__).resolve().parents[1]


def nearest_rank(values, percentile):
    if not values or not 0 < percentile <= 100:
        raise ValueError('Nonempty samples and percentile in (0, 100] required')
    return sorted(values)[math.ceil(len(values) * percentile / 100) - 1]


def request_json(url, payload, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    with urlopen(Request(url, data=json.dumps(payload).encode(), headers=headers), timeout=30) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=int, default=30)
    parser.add_argument('--warmups', type=int, default=5)
    parser.add_argument('--output', type=Path, default=ROOT/'docs/evidence/unit8/recommendation-benchmark.json')
    args = parser.parse_args()
    if args.runs < 30 or args.warmups < 0:
        raise SystemExit('Measure at least 30 runs; warmup count must be nonnegative.')
    url = os.environ.get('SKILLMATCH_BENCHMARK_DATABASE_URL', '')
    parsed = make_url(url)
    if parsed.drivername != 'postgresql+psycopg' or not (parsed.database or '').endswith('_benchmark'):
        raise SystemExit('Set SKILLMATCH_BENCHMARK_DATABASE_URL to a disposable PostgreSQL *_benchmark database.')
    username, password = 'benchmark', secrets.token_urlsafe(24)
    env = {**os.environ, 'DATABASE_URL': url, 'SKILLMATCH_JWT_SECRET': secrets.token_urlsafe(48),
        'SKILLMATCH_LOCAL_USERS': json.dumps({username: {'user_id': str(uuid4()), 'role': 'SUPERVISOR',
                                                     'password_hash': hash_password(password)}})}
    subprocess.run([sys.executable, '-m', 'alembic', 'upgrade', 'head'], cwd=ROOT, env=env, check=True)
    engine = create_engine(url)
    active = [EmployeeProfile.model_validate(item) for item in json.loads((ROOT/'data/mock/employees.json').read_text()) if item['status'] == 'ACTIVE']
    job = JobProfile.model_validate(json.loads((ROOT/'data/mock/jobs.json').read_text())[0])
    with Session(engine) as session:
        # No destructive reset: refuse occupied profile/taxonomy tables.
        if session.exec(select(EmployeeRecord)).first() or session.exec(select(JobRecord)).first() or session.exec(select(SkillRecord)).first():
            raise SystemExit('Benchmark requires an empty disposable profile/taxonomy database.')
        session.add_all([SkillRecord(skill_id=code) for code in json.loads((ROOT/'data/mock/skills.json').read_text())])
        for index in range(100):
            profile = active[index % len(active)].model_copy(update={
                'id': str(uuid5(NAMESPACE_URL, f'skillmatch-benchmark-{index}')),
                'employee_number': f'BENCH-{index:03}', 'name': f'Benchmark candidate {index:03}',
            })
            session.add(EmployeeRecord(id=profile.id, employee_number=profile.employee_number,
                                       version=profile.version, payload=profile.model_dump(mode='json')))
        session.add(JobRecord(id=job.id, job_code=job.job_code, version=job.version, payload=job.model_dump(mode='json')))
        session.commit()
        database_version = session.execute(text('SELECT version()')).scalar_one()
    port = free_port()
    samples, run_ids = [], []
    options = {'topK': 100, 'minimumScore': 0, 'includeIneligible': True, 'includeMissingSkills': True}
    with tempfile.TemporaryDirectory(prefix='skillmatch-benchmark-') as directory:
        with (Path(directory)/'server.log').open('w') as logs:
            server = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'skillmatch.main:app', '--host',
                '127.0.0.1', '--port', str(port)], cwd=ROOT, env=env, stdout=logs, stderr=logs)
            try:
                wait_ready(f'http://127.0.0.1:{port}/health', server)
                token = request_json(f'http://127.0.0.1:{port}/api/v1/auth/login', {'username': username, 'password': password})['access_token']
                endpoint = f'http://127.0.0.1:{port}/api/v1/jobs/{job.id}/recommendations'
                for index in range(args.warmups + args.runs):
                    started = time.perf_counter()
                    body = request_json(endpoint, options, token)
                    elapsed = time.perf_counter() - started
                    assert len(body['recommendations']) == 100
                    assert body['model_version'] == 'rpce-55-20-15-10-v1'
                    if index >= args.warmups:
                        samples.append(elapsed)
                        run_ids.append(body['match_run_id'])
            finally:
                server.terminate()
                try:
                    server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait()
    with engine.connect() as connection:
        persisted = [connection.execute(text('SELECT COUNT(*) FROM candidateresult WHERE match_run_id = :id'), {'id': identifier}).scalar_one() for identifier in run_ids]
    assert persisted == [100] * args.runs
    digest = hashlib.sha256()
    for path in sorted((ROOT/'backend/src/skillmatch').rglob('*.py')):
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(path.read_bytes())
    p95 = nearest_rank(samples, 95)
    report = {
        'observed_at_utc': datetime.now(timezone.utc).isoformat(),
        'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'worktree_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip()),
        'backend_source_sha256': digest.hexdigest(),
        'environment': {'python': platform.python_version(), 'platform': platform.platform(),
                        'logical_cpu_count': os.cpu_count(), 'postgresql': database_version,
                        'uvicorn_workers': 1, 'concurrent_clients': 1},
        'scope': 'Loopback HTTP, bearer validation, PostgreSQL profile reads, matching/explanations, committed run/results, response decode. Login and fixture/migration setup excluded.',
        'fixture': '100 ACTIVE profiles cyclically cloned from the nine ACTIVE mock profiles; one Commercial Electrician job; all 100 candidates returned/persisted, including ineligible candidates.',
        'active_profile_count': 100, 'measured_runs': args.runs, 'warmup_runs_excluded': args.warmups,
        'options': options, 'model_version': 'rpce-55-20-15-10-v1', 'latency_seconds': samples,
        'measured_match_run_ids': run_ids, 'persisted_candidate_counts': persisted,
        'median_seconds': nearest_rank(samples, 50), 'p95_seconds': p95,
        'minimum_seconds': min(samples), 'maximum_seconds': max(samples),
        'percentile_method': 'nearest rank: sorted samples[ceil(n * p / 100) - 1]',
        'target_p95_seconds': 2, 'target_met': p95 < 2,
        'limitations': 'Synthetic single-job, sequential local warm-cache test. Not production load, multi-user scalability, network latency, or staffing-relevance evidence.',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    engine.dispose()
    print(f'100 ACTIVE profiles, {args.runs} runs: P95 {p95:.6f}s; target <2s: {report["target_met"]}')
    if not report['target_met']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
