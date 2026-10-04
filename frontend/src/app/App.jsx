import React, { useEffect, useSyncExternalStore } from 'react';
import LoginPage from '../features/auth/LoginPage';
import { clearSession, getSession, subscribe } from '../features/auth/session';
import './styles.css';

export default function App() {
  const session = useSyncExternalStore(subscribe, getSession);
  useEffect(() => {
    if (!session) return;
    const timer = setTimeout(clearSession, Math.max(0, session.expiresAt - Date.now()));
    return () => clearTimeout(timer);
  }, [session]);

  return <main className="portal">
    <aside className="brand-panel">
      <a className="brand" href="/" aria-label="SkillMatch home"><span className="brand-mark" aria-hidden="true">S</span>SkillMatch<span className="ai-badge">AI</span></a>
      <div className="brand-story">
        <p className="eyebrow">SKILLS FIRST. PEOPLE ALWAYS.</p>
        <h2>The right skills.<br />The right opportunity.</h2>
        <p>Bring skills, experience, and opportunity together. Make informed workforce decisions with clear, human-reviewed recommendations.</p>
        <div className="evidence-card"><span className="evidence-icon" aria-hidden="true">✓</span><div><strong>Evidence you can understand</strong><p>Transparent matching. Supervisor-led decisions.</p></div></div>
      </div>
      <footer>Decision support, with people in control.</footer>
    </aside>
    <div className="form-area">
      {session ? <section className="login-panel" aria-labelledby="signed-in-title">
        <p className="eyebrow">WORKSPACE</p><h1 id="signed-in-title">You’re signed in</h1>
        <p className="intro">Welcome to your workspace. Your session is active.</p>
        <button className="primary" onClick={clearSession}>Sign out<span aria-hidden="true">↗</span></button>
      </section> : <LoginPage />}
      <p className="form-footer">SkillMatch AI · Workforce decision support</p>
    </div>
  </main>;
}
