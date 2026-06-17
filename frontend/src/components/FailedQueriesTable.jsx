const thStyle = {
  padding: '0.6rem 0.9rem',
  textAlign: 'left',
  fontSize: '0.78rem',
  fontWeight: '700',
  color: '#64748b',
  textTransform: 'uppercase',
  letterSpacing: '0.04em',
  borderBottom: '2px solid #e2e8f0',
  background: '#f8fafc',
}

const tdStyle = {
  padding: '0.65rem 0.9rem',
  fontSize: '0.87rem',
  borderBottom: '1px solid #f1f5f9',
}

export default function FailedQueriesTable({ data }) {
  return (
    <div
      style={{
        background: '#fff',
        border: '1px solid #e2e8f0',
        borderRadius: '10px',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          padding: '1rem 1.25rem',
          borderBottom: '1px solid #f1f5f9',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
        }}
      >
        <h3 style={{ fontSize: '0.9rem', fontWeight: '700', color: '#374151' }}>
          Unanswered Questions
        </h3>
        {data && data.length > 0 && (
          <span
            style={{
              background: '#fee2e2',
              color: '#991b1b',
              borderRadius: '4px',
              padding: '0.1rem 0.5rem',
              fontSize: '0.75rem',
              fontWeight: '700',
            }}
          >
            {data.length}
          </span>
        )}
      </div>

      {!data || data.length === 0 ? (
        <div style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.9rem' }}>
          No failed queries. The document covers all questions asked so far.
        </div>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={thStyle}>Question</th>
                <th style={{ ...thStyle, textAlign: 'right' }}>Count</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, i) => (
                <tr key={i}>
                  <td style={tdStyle}>{row.query}</td>
                  <td style={{ ...tdStyle, textAlign: 'right', fontWeight: '700', color: '#dc2626' }}>
                    {row.count}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
