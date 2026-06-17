import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

export default function DailyQueryChart({ data }) {
  if (!data || data.length === 0) {
    return <EmptyState label="No daily data yet." />
  }

  return (
    <div
      style={{
        background: '#fff',
        border: '1px solid #e2e8f0',
        borderRadius: '10px',
        padding: '1.25rem',
      }}
    >
      <h3 style={{ fontSize: '0.9rem', fontWeight: '700', marginBottom: '1rem', color: '#374151' }}>
        Daily Query Volume (last 30 days)
      </h3>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} margin={{ top: 4, right: 8, left: -16, bottom: 4 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 11, fill: '#94a3b8' }}
            tickFormatter={(v) => v.slice(5)} // show MM-DD
          />
          <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: '#94a3b8' }} />
          <Tooltip
            contentStyle={{ fontSize: '0.82rem', borderRadius: '6px', border: '1px solid #e2e8f0' }}
            labelStyle={{ fontWeight: '700' }}
          />
          <Bar dataKey="count" fill="#3b82f6" radius={[3, 3, 0, 0]} name="Queries" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

function EmptyState({ label }) {
  return (
    <div
      style={{
        background: '#fff',
        border: '1px solid #e2e8f0',
        borderRadius: '10px',
        padding: '2rem',
        textAlign: 'center',
        color: '#94a3b8',
        fontSize: '0.9rem',
      }}
    >
      {label}
    </div>
  )
}
