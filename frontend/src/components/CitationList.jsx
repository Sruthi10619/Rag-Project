import { useState } from 'react'

function Citation({ source, index }) {
  const [open, setOpen] = useState(false)

  return (
    <div
      style={{
        border: '1px solid #e2e8f0',
        borderRadius: '8px',
        padding: '0.75rem 1rem',
        background: '#f8fafc',
      }}
    >
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          cursor: 'pointer',
        }}
        onClick={() => setOpen((o) => !o)}
      >
        <span style={{ fontSize: '0.88rem', fontWeight: '600' }}>
          <span
            style={{
              background: '#dbeafe',
              color: '#1d4ed8',
              borderRadius: '4px',
              padding: '0.15rem 0.5rem',
              marginRight: '0.5rem',
            }}
          >
            Page {source.page}
          </span>
          Chunk {source.chunk_id}
        </span>
        <span style={{ fontSize: '0.78rem', color: '#64748b' }}>
          {open ? '▲ hide' : '▼ excerpt'}
        </span>
      </div>

      {open && (
        <blockquote
          style={{
            marginTop: '0.6rem',
            padding: '0.6rem 0.9rem',
            background: '#fff',
            border: '1px solid #e2e8f0',
            borderLeft: '3px solid #3b82f6',
            borderRadius: '4px',
            fontStyle: 'italic',
            fontSize: '0.84rem',
            color: '#475569',
            lineHeight: '1.6',
          }}
        >
          "{source.snippet}"
        </blockquote>
      )}
    </div>
  )
}

export default function CitationList({ sources }) {
  if (!sources || sources.length === 0) return null

  return (
    <div style={{ marginTop: '1.25rem' }}>
      <h3
        style={{
          fontSize: '0.85rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#64748b',
          marginBottom: '0.6rem',
        }}
      >
        Sources ({sources.length})
      </h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {sources.map((s, i) => (
          <Citation key={`${s.page}-${s.chunk_id}`} source={s} index={i} />
        ))}
      </div>
    </div>
  )
}
