import React, { useRef, useState } from 'react';
import { apiRequest } from '../../api/client';
import ProblemAlert, {uiProblem} from '../../components/ProblemAlert';
import { setSession } from './session';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  const submitting = useRef(false);

  async function submit(event) {
    event.preventDefault();
    if (submitting.current) return;
    submitting.current = true;
    setPending(true);
    setError('');
    try {
      const token = await apiRequest('/auth/login', {
        method: 'POST', auth: false, body: { username, password },
      });
      setPassword('');
      setSession(token);
    } catch (failure) {
      setPassword('');
      setError(uiProblem(failure, failure.status === 401 ? 'Invalid username or password.' : 'Unable to sign in. Please try again.'));
    } finally {
      submitting.current = false;
      setPending(false);
    }
  }

  return <section className="login-panel" aria-labelledby="login-title">
    <p className="eyebrow">SUPERVISOR PORTAL</p>
    <h1 id="login-title">Welcome back</h1>
    <p className="intro">Sign in to your SkillMatch workspace.</p>
    <form onSubmit={submit} aria-busy={pending}>
      <label htmlFor="username">Username</label>
      <input id="username" name="username" autoComplete="username" autoCapitalize="none"
        aria-describedby={error ? "login-error" : undefined} spellCheck={false} required maxLength={128} value={username}
        onChange={event => setUsername(event.target.value)} disabled={pending} />
      <label htmlFor="password">Password</label>
      <input id="password" name="password" type="password" autoComplete="current-password"
        aria-describedby={error ? "login-error" : undefined} required maxLength={1024} value={password} onChange={event => setPassword(event.target.value)} disabled={pending} />
      {error && <ProblemAlert id="login-error" error={error} fieldTargets={{username: 'username', password: 'password'}} />}
      <button className="primary" type="submit" disabled={pending}>{pending ? 'Signing in…' : 'Sign in'}<span aria-hidden="true">↗</span></button>
    </form>
    <p className="access-note">Need access? Contact your administrator.</p>
  </section>;
}
