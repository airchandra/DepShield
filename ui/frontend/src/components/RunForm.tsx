import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'
import { RunRequest } from '../types'

const ECOSYSTEMS = ['jvm', 'python', 'javascript', 'go', 'rust']

export default function RunForm() {
  const navigate = useNavigate()
  const [repos, setRepos] = useState('')
  const [dryRun, setDryRun] = useState(true)
  const [selectedEcosystems, setSelectedEcosystems] = useState(ECOSYSTEMS)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleEcosystemToggle = (eco: string) => {
    setSelectedEcosystems((prev) =>
      prev.includes(eco) ? prev.filter((e) => e !== eco) : [...prev, eco]
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const repoList = repos
        .split('\n')
        .map((r) => r.trim())
        .filter((r) => r.length > 0)

      if (repoList.length === 0) {
        setError('Please enter at least one repository path')
        setLoading(false)
        return
      }

      const request: RunRequest = {
        repos: repoList,
        dry_run: dryRun,
        apply: !dryRun,
        ecosystems: selectedEcosystems,
      }

      const { id } = await api.createRun(request)
      navigate(`/runs/${id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create run')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">New Scan</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Repositories */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Repository Paths
          </label>
          <textarea
            value={repos}
            onChange={(e) => setRepos(e.target.value)}
            placeholder="Enter repo paths, one per line&#10;Example:&#10;./api&#10;./frontend&#10;./services/data"
            className="w-full h-32 p-3 border border-gray-300 rounded-lg font-mono text-sm"
            disabled={loading}
          />
        </div>

        {/* Mode */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Execution Mode</label>
          <div className="flex gap-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="mode"
                checked={dryRun}
                onChange={() => setDryRun(true)}
                disabled={loading}
              />
              <span>Dry Run (scan only)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="mode"
                checked={!dryRun}
                onChange={() => setDryRun(false)}
                disabled={loading}
              />
              <span>Apply (scan + remediate)</span>
            </label>
          </div>
        </div>

        {/* Ecosystems */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Ecosystems to Scan
          </label>
          <div className="grid grid-cols-2 gap-3">
            {ECOSYSTEMS.map((eco) => (
              <label key={eco} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedEcosystems.includes(eco)}
                  onChange={() => handleEcosystemToggle(eco)}
                  disabled={loading}
                />
                <span className="capitalize">{eco}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Error */}
        {error && <div className="p-3 bg-red-100 border border-red-400 rounded text-red-700">{error}</div>}

        {/* Submit */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 rounded-lg transition"
        >
          {loading ? 'Starting...' : 'Start Scan'}
        </button>
      </form>
    </div>
  )
}
