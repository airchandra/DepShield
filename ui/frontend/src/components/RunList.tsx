import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { RunSummary } from '../types'

export default function RunList() {
  const [runs, setRuns] = useState<RunSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadRuns = async () => {
    try {
      const data = await api.listRuns()
      setRuns(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load runs')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadRuns()
    const interval = setInterval(loadRuns, 5000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (error) {
    return <div className="text-red-600 text-center py-8">{error}</div>
  }

  if (runs.length === 0) {
    return (
      <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
        <p className="text-gray-600">No scans yet. Create one to get started.</p>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-blue-100 text-blue-800'
      case 'done':
        return 'bg-green-100 text-green-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Recent Scans</h2>
      <div className="space-y-3">
        {runs.map((run) => (
          <Link key={run.id} to={`/runs/${run.id}`}>
            <div className="p-4 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition cursor-pointer">
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-sm text-gray-600">{run.id}</span>
                <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusColor(run.status)}`}>
                  {run.status.toUpperCase()}
                </span>
              </div>
              <p className="text-sm text-gray-700 mb-2">{run.total_repos} repos • {run.total_dependencies} deps • {run.total_vulnerabilities} vulns</p>
              <p className="text-xs text-gray-500">
                {new Date(run.started_at).toLocaleString()}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
