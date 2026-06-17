const NOT_FOUND = 'Information not found in the AWS Customer Agreement.'

export default function AnswerCard({ answer, answerFound, latencyMs, topScore }) {
  const notFound = !answerFound || answer === NOT_FOUND

  return (
    <div
      style={{
        background: notFound ? '#fffbeb' : '#fff',
        border: `1.5px solid ${notFound ? '#fbbf24' : '#e2e8f0'}`,
        borderRadius: '10px',
        padding: '1.25rem 1.5rem',
        marginTop: '1.25rem',
      }}
    >
      {notFound && (
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            background: '#fef3c7',
            color: '#92400e',
            borderRadius: '4px',
            padding: '0.2rem 0.6rem',
            fontSize: '0.8rem',
            fontWeight: '600',
            marginBottom: '0.75rem',
          }}
        >
          Not found
        </div>
      )}

      <p style={{ lineHeight: '1.7', fontSize: '0.97rem', whiteSpace: 'pre-wrap' }}>
        {answer}
      </p>

      <div
        style={{
          marginTop: '1rem',
          display: 'flex',
          gap: '1rem',
          fontSize: '0.78rem',
          color: '#94a3b8',
        }}
      >
        <span>Latency: {latencyMs?.toFixed(0)} ms</span>
        {topScore != null && <span>Top score: {topScore.toFixed(4)}</span>}
      </div>
    </div>
  )
}
