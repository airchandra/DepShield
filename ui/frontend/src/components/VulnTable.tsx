import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api'
import { Vulnerability } from '../types'
import SeverityBadge from './SeverityBadge'

export default function VulnTable() {
  const { id } = useParams<{ id: string }>()
  const [vulns, setVulns] = useState<Vulnerability[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [severity, setSeverity] = useState('')
  const [sort, setSort] = useState('severity')

  const loadVulns = async () => {
    try {
      const data = await api.getVulnerabilities(id!, { severity: severity || undefined, sort })
      setVulns(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load vulnerabilities')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadVulns()
  }, [id, severity, sort])

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (error) {
    return <div className="text-red-600">{error}</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Vulnerabilities</h1>

      {/* Filters */}
      <div className="flex gap-4 mb-6">
        <select
          value={severity}
          onChange={(e) => setSeverity(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded"
        >
          <option value="">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>

        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded"
        >
          <option value="severity">Sort by Severity</option>
          <option value="cvss_score">Sort by CVSS</option>
          <option value="package">Sort by Package</option>
        </select>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-100 border-b">
            <tr>
              <th className="px-4 py-2 text-left">CVE</th>
              <th className="px-4 py-2 text-left">Package</th>
              <th className="px-4 py-2 text-left">Severity</th>
              <th className="px-4 py-2 text-left">CVSS</th>
              <th className="px-4 py-2 text-left">Current</th>
              <th className="px-4 py-2 text-left">Fixed</th>
            </tr>
          </thead>
          <tbody>
            {vulns.map((vuln) => (
              <tr key={vuln.id} className="border-b hover:bg-gray-50">
                <td className="px-4 py-2 font-mono text-xs">{vuln.id}</td>
                <td className="px-4 py-2">{vuln.package}</td>
                <td className="px-4 py-2">
                  <SeverityBadge severity={vuln.severity} />
                </td>
                <td className="px-4 py-2 font-semibold">{vuln.cvss_score.toFixed(1)}</td>
                <td className="px-4 py-2 font-mono text-xs">{vuln.current_version}</td>
                <td className="px-4 py-2 font-mono text-xs text-green-600">{vuln.fixed_version}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="mt-4 text-gray-600">Total: {vulns.length} vulnerabilities</p>
    </div>
  )
}
