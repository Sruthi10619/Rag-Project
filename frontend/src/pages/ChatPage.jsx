import { useState } from 'react'
import AnswerCard from '../components/AnswerCard'
import ChatInput from '../components/ChatInput'
import CitationList from '../components/CitationList'
import { askQuestion } from '../services/api'

export default function ChatPage() {
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async () => {
    const q = question.trim()
    if (q.length < 3) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await askQuestion(q)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '780px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '1.4rem', fontWeight: '800', marginBottom: '0.4rem', color: '#0f172a' }}>
        AWS Customer Agreement QA
      </h1>
      <p style={{ color: '#64748b', fontSize: '0.92rem', marginBottom: '1.5rem' }}>
        Ask any question about the AWS Customer Agreement. Answers are grounded in the
        document — no hallucination.
      </p>

      <ChatInput
        value={question}
        onChange={setQuestion}
        onSubmit={handleSubmit}
        loading={loading}
      />

      {loading && (
        <div
          style={{
            marginTop: '1.25rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            color: '#475569',
            fontSize: '0.9rem',
          }}
        >
          <Spinner />
          Searching document and generating answer…
        </div>
      )}

      {error && (
        <div
          style={{
            marginTop: '1.25rem',
            background: '#fef2f2',
            border: '1px solid #fecaca',
            borderRadius: '8px',
            padding: '1rem 1.25rem',
            color: '#991b1b',
            fontSize: '0.9rem',
          }}
        >
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && !loading && (
        <>
          <AnswerCard
            answer={result.answer}
            answerFound={result.answer_found}
            latencyMs={result.latency_ms}
            topScore={result.top_score}
          />
          <CitationList sources={result.sources} />
          {result.tokens_prompt != null && (
            <div style={{ marginTop: '0.75rem', fontSize: '0.76rem', color: '#94a3b8' }}>
              Tokens — prompt: {result.tokens_prompt} / completion: {result.tokens_completion}
            </div>
          )}
        </>
      )}
    </div>
  )
}

function Spinner() {
  return (
    <div
      style={{
        width: '18px',
        height: '18px',
        border: '3px solid #e2e8f0',
        borderTop: '3px solid #3b82f6',
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite',
      }}
    >
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  )
}
