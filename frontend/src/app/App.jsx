import React, { useEffect, useState, useSyncExternalStore } from 'react';
import LoginPage from '../features/auth/LoginPage';
import JobListPage from '../features/jobs/JobListPage';
import { clearSession, getSession, subscribe } from '../features/auth/session';
import ProfilesPage from '../features/profiles/ProfilesPage';
import './styles.css';
import '../styles.css';

export default function App() {
  const [page, setPage] = useState('recommendations');
  const session = useSyncExternalStore(subscribe, getSession);
  useEffect(() => {
    if (!session) return;
    const timer = setTimeout(clearSession, Math.max(0, session.expiresAt - Date.now()));
    return () => clearTimeout(timer);
  }, [session]);

  if (session) return <>
    <nav className="portal-navigation" aria-label="Workspace pages">
      <button aria-pressed={page === 'recommendations'} onClick={() => setPage('recommendations')}>Job recommendations</button>
      <button aria-pressed={page === 'employees'} onClick={() => setPage('employees')}>Employee profiles</button>
      <button aria-pressed={page === 'jobs'} onClick={() => setPage('jobs')}>Job profiles</button>
    </nav>
    {page === 'recommendations' ? <JobListPage onLogout={clearSession} /> : <main className="profile-workspace"><header><h1>SkillMatch</h1><button className="secondary" onClick={clearSession}>Sign out</button></header><ProfilesPage key={page} kind={page} /></main>}
  </>;

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
      <LoginPage />
      <p className="form-footer">SkillMatch AI · Workforce decision support</p>
    </div>
  </main>;
}
