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
  verticalAlign: 'top',
}

export default function RecentQueriesTable({ data }) {
  return (
    <div
      style={{
        background: '#fff',
        border: '1px solid #e2e8f0',
        borderRadius: '10px',
        overflow: 'hidden',
      }}
    >
      <div style={{ padding: '1rem 1.25rem', borderBottom: '1px solid #f1f5f9' }}>
        <h3 style={{ fontSize: '0.9rem', fontWeight: '700', color: '#374151' }}>
          Recent Queries
        </h3>
      </div>
      {!data || data.length === 0 ? (
        <div style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.9rem' }}>
          No queries yet.
        </div>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={thStyle}>Time</th>
                <th style={thStyle}>Question</th>
                <th style={thStyle}>Found</th>
                <th style={thStyle}>Latency</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row) => (
                <tr key={row.id}>
                  <td style={{ ...tdStyle, whiteSpace: 'nowrap', color: '#94a3b8', fontSize: '0.78rem' }}>
                    {new Date(row.created_at).toLocaleString()}
                  </td>
                  <td style={tdStyle}>{row.query}</td>
                  <td style={tdStyle}>
                    <span
                      style={{
                        display: 'inline-block',
                        padding: '0.1rem 0.5rem',
                        borderRadius: '4px',
                        fontSize: '0.78rem',
                        fontWeight: '600',
                        background: row.answer_found ? '#dcfce7' : '#fee2e2',
                        color: row.answer_found ? '#166534' : '#991b1b',
                      }}
                    >
                      {row.answer_found ? 'Yes' : 'No'}
                    </span>
                  </td>
                  <td style={{ ...tdStyle, whiteSpace: 'nowrap', color: '#64748b' }}>
                    {row.latency_ms?.toFixed(0)} ms
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
