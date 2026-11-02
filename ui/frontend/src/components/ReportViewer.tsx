import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import { api } from '../api'
import mermaid from 'mermaid'

const REPORT_FILES = [
  'SBOM.md',
  'VULNERABILITY_REPORT.md',
  'ARCHITECTURE.md',
  'CODING_GUIDELINES.md',
  'SEQUENCE_DIAGRAMS.md',
  'TEST_CASES.md',
  'UPGRADE_PLAN.md',
]

export default function ReportViewer() {
  const { id, repo } = useParams<{ id: string; repo: string }>()
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [file, setFile] = useState('SBOM.md')

  const loadReport = async () => {
    try {
      setLoading(true)
      const text = await api.getReport(id!, repo!, file)
      setContent(text)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load report')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadReport()
  }, [id, repo, file])

  useEffect(() => {
    mermaid.contentLoaded()
  }, [content])

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
      {/* Sidebar */}
      <div className="md:col-span-1">
        <h3 className="font-bold text-lg mb-4">Reports</h3>
        <div className="space-y-2">
          {REPORT_FILES.map((filename) => (
            <button
              key={filename}
              onClick={() => setFile(filename)}
              className={`block w-full text-left px-3 py-2 rounded text-sm ${
                file === filename
                  ? 'bg-blue-600 text-white'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              {filename}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="md:col-span-3">
        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : error ? (
          <div className="text-red-600">{error}</div>
        ) : (
          <div className="bg-white rounded-lg border border-gray-200 p-6 markdown">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeHighlight]}
              components={{
                code: ({ node, inline, className, children, ...props }) => {
                  const match = /language-(\w+)/.exec(className || '')
                  // Check if it's a mermaid diagram
                  if (inline === false && match && match[1] === 'mermaid') {
                    return (
                      <div className="mermaid">
                        {String(children).replace(/\n$/, '')}
                      </div>
                    )
                  }
                  return (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  )
                },
              }}
            >
              {content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  )
}
