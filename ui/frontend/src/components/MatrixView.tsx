import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api'
import { DependencyMatrixRow, UpgradeMatrixRow } from '../types'
import SeverityBadge from './SeverityBadge'

export default function MatrixView() {
  const { id } = useParams<{ id: string }>()
  const [depMatrix, setDepMatrix] = useState<DependencyMatrixRow[]>([])
  const [upgradeMatrix, setUpgradeMatrix] = useState<UpgradeMatrixRow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [tab, setTab] = useState<'dep' | 'upgrade'>('dep')

  const loadMatrices = async () => {
    try {
      const [deps, upgrades] = await Promise.all([
        api.getDependencyMatrix(id!),
        api.getUpgradeMatrix(id!),
      ])
      setDepMatrix(deps)
      setUpgradeMatrix(upgrades)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load matrices')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadMatrices()
  }, [id])

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (error) {
    return <div className="text-red-600">{error}</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Matrices</h1>

      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b">
        <button
          onClick={() => setTab('dep')}
          className={`px-4 py-2 font-semibold ${tab === 'dep' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
        >
          Dependencies ({depMatrix.length})
        </button>
        <button
          onClick={() => setTab('upgrade')}
          className={`px-4 py-2 font-semibold ${tab === 'upgrade' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
        >
          Upgrades ({upgradeMatrix.length})
        </button>
      </div>

      {/* Dependency Matrix */}
      {tab === 'dep' && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-100 border-b sticky top-0">
              <tr>
                <th className="px-4 py-2 text-left">Package</th>
                <th className="px-4 py-2 text-left">Repos</th>
                <th className="px-4 py-2 text-left">Versions</th>
              </tr>
            </thead>
            <tbody>
              {depMatrix.map((row) => (
                <tr key={row.package} className={`border-b hover:bg-gray-50 ${row.has_conflict ? 'bg-yellow-50' : ''}`}>
                  <td className="px-4 py-2 font-semibold">{row.package}</td>
                  <td className="px-4 py-2 text-sm">{row.repos.join(', ')}</td>
                  <td className="px-4 py-2 text-xs font-mono">
                    {Object.entries(row.versions)
                      .map(([repo, versions]) => `${versions.join(', ')}`)
                      .join(' | ')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Upgrade Matrix */}
      {tab === 'upgrade' && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-100 border-b sticky top-0">
              <tr>
                <th className="px-4 py-2 text-left">Package</th>
                <th className="px-4 py-2 text-left">Current</th>
                <th className="px-4 py-2 text-left">Safe Version</th>
                <th className="px-4 py-2 text-left">Severity</th>
                <th className="px-4 py-2 text-left">CVSS</th>
                <th className="px-4 py-2 text-left">CVEs</th>
              </tr>
            </thead>
            <tbody>
              {upgradeMatrix.map((row) => (
                <tr key={row.package} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-2 font-semibold">{row.package}</td>
                  <td className="px-4 py-2 font-mono text-xs">{row.current_version}</td>
                  <td className="px-4 py-2 font-mono text-xs text-green-600">{row.safe_version}</td>
                  <td className="px-4 py-2">
                    <SeverityBadge severity={row.severity as any} />
                  </td>
                  <td className="px-4 py-2 font-semibold">{row.cvss_score.toFixed(1)}</td>
                  <td className="px-4 py-2 text-xs">{row.cve_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
