import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api'
import { RunResponse } from '../types'
import ScanLog from './ScanLog'
import EcosystemChip from './EcosystemChip'

export default function RunDetail() {
  const { id } = useParams<{ id: string }>()
  const [run, setRun] = useState<RunResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadRun = async () => {
    try {
      const data = await api.getRun(id!)
      setRun(data)
      if (data.status !== 'running') {
        setLoading(false)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load run')
      setLoading(false)
    }
  }

  useEffect(() => {
    loadRun()
    const interval = setInterval(loadRun, 3000)
    return () => clearInterval(interval)
  }, [id])

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (error) {
    return <div className="text-red-600">{error}</div>
  }

  if (!run) {
    return <div>Run not found</div>
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
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Scan {run.id}</h1>
        <span className={`px-3 py-1 rounded-full font-semibold ${getStatusColor(run.status)}`}>
          {run.status.toUpperCase()}
        </span>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <p className="text-gray-600 text-sm">Repositories</p>
          <p className="text-2xl font-bold">{run.repos.length}</p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <p className="text-gray-600 text-sm">Dependencies</p>
          <p className="text-2xl font-bold">{run.total_dependencies}</p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <p className="text-gray-600 text-sm">Vulnerabilities</p>
          <p className="text-2xl font-bold text-red-600">{run.total_vulnerabilities}</p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <p className="text-gray-600 text-sm">Mode</p>
          <p className="text-xl font-bold">{run.dry_run ? 'Dry-Run' : 'Apply'}</p>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex gap-2 mb-6">
        <Link
          to={`/runs/${run.id}/vulns`}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          View Vulnerabilities
        </Link>
        <Link
          to={`/runs/${run.id}/matrix`}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          View Matrices
        </Link>
      </div>

      {/* Log Stream */}
      <div className="bg-white rounded-lg border border-gray-200 p-4 mb-8">
        <h2 className="text-lg font-bold mb-4">Live Log</h2>
        <ScanLog runId={run.id} />
      </div>

      {/* Error Message */}
      {run.error_message && (
        <div className="bg-red-100 border border-red-400 text-red-700 p-4 rounded">
          {run.error_message}
        </div>
      )}
    </div>
  )
}
