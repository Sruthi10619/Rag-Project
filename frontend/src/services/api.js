import axios from 'axios'

// All requests go through the Vite /api proxy → http://localhost:8000
const client = axios.create({
  baseURL: '/api',
  timeout: 90_000, // LLM calls can take up to 30s
  headers: { 'Content-Type': 'application/json' },
})

// Normalize errors so callers always receive an Error object with a message string
client.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const detail = err.response?.data?.detail
    const msg =
      typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
        ? detail.map((d) => d.msg).join('; ')
        : err.message || 'Unknown error'
    return Promise.reject(new Error(msg))
  },
)

/** Ask a question about the AWS Customer Agreement. */
export const askQuestion = (question) => client.post('/ask', { question })

/** Fetch aggregated analytics. */
export const getAnalytics = () => client.get('/analytics')

/**
 * Ingest the PDF.
 * @param {File|null} file  - Upload a file, or pass null to use the server-side PDF_PATH.
 * @param {boolean} force   - Delete existing vectors and re-ingest.
 */
export const ingestPdf = (file = null, force = false) => {
  const params = force ? '?force_reingest=true' : ''
  if (file) {
    const form = new FormData()
    form.append('file', file)
    return client.post(`/ingest${params}`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  }
  return client.post(`/ingest${params}`)
}

/** Health probe. */
export const getHealth = () => client.get('/health')
