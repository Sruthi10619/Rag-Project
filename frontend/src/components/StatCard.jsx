export default function StatCard({ title, value, subtitle, accent = '#3b82f6' }) {
  return (
    <div
      style={{
        background: '#fff',
        border: '1px solid #e2e8f0',
        borderTop: `4px solid ${accent}`,
        borderRadius: '10px',
        padding: '1.25rem 1.5rem',
        flex: '1 1 180px',
        minWidth: '150px',
      }}
    >
      <div style={{ fontSize: '0.78rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
        {title}
      </div>
      <div style={{ fontSize: '2rem', fontWeight: '800', margin: '0.35rem 0', color: '#0f172a' }}>
        {value ?? '—'}
      </div>
      {subtitle && (
        <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>{subtitle}</div>
      )}
    </div>
  )
}
