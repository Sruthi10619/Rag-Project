import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const COLORS = ['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe']

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const { query, count } = payload[0].payload
  return (
    <div
      style={{
        background: '#fff',
        border: '1px solid #e2e8f0',
        borderRadius: '6px',
        padding: '0.6rem 0.8rem',
        maxWidth: '280px',
        fontSize: '0.82rem',
      }}
    >
      <div style={{ fontWeight: '700', marginBottom: '0.3rem' }}>{count} queries</div>
      <div style={{ color: '#475569', lineHeight: '1.4' }}>{query}</div>
    </div>
  )
}

export default function TopQuestionsChart({ data }) {
  if (!data || data.length === 0) {
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
        No questions asked yet.
      </div>
    )
  }

  const chartData = data.map((d) => ({
    ...d,
    label: d.query.length > 40 ? d.query.slice(0, 40) + '…' : d.query,
  }))

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
        Top Questions
      </h3>
      <ResponsiveContainer width="100%" height={Math.max(200, chartData.length * 38)}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 4, right: 24, left: 8, bottom: 4 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
          <XAxis type="number" allowDecimals={false} tick={{ fontSize: 11, fill: '#94a3b8' }} />
          <YAxis
            type="category"
            dataKey="label"
            width={180}
            tick={{ fontSize: 11, fill: '#475569' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="count" radius={[0, 3, 3, 0]} name="Count">
            {chartData.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
