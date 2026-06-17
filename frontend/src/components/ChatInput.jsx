export default function ChatInput({ value, onChange, onSubmit, loading }) {
  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (!loading && value.trim().length >= 3) onSubmit()
    }
  }

  return (
    <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKey}
        placeholder="Ask a question about the AWS Customer Agreement…"
        rows={3}
        disabled={loading}
        style={{
          flex: 1,
          padding: '0.85rem 1rem',
          fontSize: '0.95rem',
          border: '1.5px solid #d1d5db',
          borderRadius: '8px',
          resize: 'vertical',
          outline: 'none',
          fontFamily: 'inherit',
          background: loading ? '#f9fafb' : '#fff',
          transition: 'border-color 0.15s',
        }}
        onFocus={(e) => (e.target.style.borderColor = '#3b82f6')}
        onBlur={(e) => (e.target.style.borderColor = '#d1d5db')}
      />
      <button
        onClick={onSubmit}
        disabled={loading || value.trim().length < 3}
        style={{
          padding: '0.85rem 1.5rem',
          background:
            loading || value.trim().length < 3 ? '#93c5fd' : '#2563eb',
          color: '#fff',
          border: 'none',
          borderRadius: '8px',
          fontWeight: '600',
          fontSize: '0.95rem',
          minWidth: '90px',
          transition: 'background 0.15s',
        }}
      >
        {loading ? '…' : 'Ask'}
      </button>
    </div>
  )
}
