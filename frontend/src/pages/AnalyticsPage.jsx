import { useEffect, useState } from 'react'
import DailyQueryChart from '../components/DailyQueryChart'
import FailedQueriesTable from '../components/FailedQueriesTable'
import RecentQueriesTable from '../components/RecentQueriesTable'
import StatCard from '../components/StatCard'
import TopQuestionsChart from '../components/TopQuestionsChart'
import { getAnalytics } from '../services/api'

export default function AnalyticsPage() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getAnalytics()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem', color: '#94a3b8' }}>
        Loading analytics…
      </div>
    )
  }

  if (error) {
    return (
      <div
        style={{
          background: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '8px',
          padding: '1.25rem',
          color: '#991b1b',
        }}
      >
        Failed to load analytics: {error}
      </div>
    )
  }

  const successPct =
    data.success_rate != null ? (data.success_rate * 100).toFixed(1) + '%' : '—'

  const avgLatency =
    data.avg_latency_ms != null ? data.avg_latency_ms.toFixed(0) + ' ms' : '—'

  const avgScore =
    data.avg_retrieval_score != null ? data.avg_retrieval_score.toFixed(4) : '—'

  return (
    <div>
      <h1 style={{ fontSize: '1.4rem', fontWeight: '800', marginBottom: '1.5rem', color: '#0f172a' }}>
        Analytics Dashboard
      </h1>

      {/* ── Stat cards ── */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
        <StatCard
          title="Total Requests"
          value={data.total_requests}
          accent="#3b82f6"
        />
        <StatCard
          title="Success Rate"
          value={successPct}
          subtitle="Answer found in document"
          accent="#22c55e"
        />
        <StatCard
          title="Avg Latency"
          value={avgLatency}
          subtitle="End-to-end response time"
          accent="#f59e0b"
        />
        <StatCard
          title="Avg Retrieval Score"
          value={avgScore}
          subtitle="Cosine similarity (0–1)"
          accent="#8b5cf6"
        />
      </div>

      {/* ── Charts ── */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '1.25rem',
          marginBottom: '1.5rem',
        }}
      >
        <DailyQueryChart data={data.daily_query_counts} />
        <TopQuestionsChart data={data.top_questions} />
      </div>

      {/* ── Tables ── */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '1.25rem',
        }}
      >
        <RecentQueriesTable data={data.recent_queries} />
        <FailedQueriesTable data={data.failed_queries} />
      </div>
    </div>
  )
}
