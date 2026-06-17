import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom'
import AnalyticsPage from './pages/AnalyticsPage'
import ChatPage from './pages/ChatPage'

const navStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: '1.5rem',
  padding: '0.85rem 2rem',
  background: '#1a1a2e',
  color: '#fff',
  boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
}

const linkStyle = ({ isActive }) => ({
  color: isActive ? '#60a5fa' : '#cbd5e1',
  fontWeight: isActive ? '700' : '400',
  fontSize: '0.95rem',
  paddingBottom: '2px',
  borderBottom: isActive ? '2px solid #60a5fa' : '2px solid transparent',
  transition: 'color 0.15s',
})

export default function App() {
  return (
    <BrowserRouter>
      <nav style={navStyle}>
        <span style={{ fontWeight: '800', fontSize: '1.05rem', marginRight: '1rem' }}>
          AWS Agreement QA
        </span>
        <NavLink to="/" style={linkStyle}>
          Chat
        </NavLink>
        <NavLink to="/analytics" style={linkStyle}>
          Analytics
        </NavLink>
      </nav>

      <main style={{ maxWidth: '1100px', margin: '0 auto', padding: '2rem 1rem' }}>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}
