import {
  DependencyMatrixRow,
  RunRequest,
  RunResponse,
  RunSummary,
  UpgradeMatrixRow,
  Vulnerability,
} from './types'

const API_BASE = '/api'

export const api = {
  // Runs
  async createRun(req: RunRequest): Promise<{ id: string }> {
    const res = await fetch(`${API_BASE}/runs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req),
    })
    if (!res.ok) throw new Error(`Failed to create run: ${res.statusText}`)
    return res.json()
  },

  async listRuns(): Promise<RunSummary[]> {
    const res = await fetch(`${API_BASE}/runs`)
    if (!res.ok) throw new Error(`Failed to list runs: ${res.statusText}`)
    return res.json()
  },

  async getRun(runId: string): Promise<RunResponse> {
    const res = await fetch(`${API_BASE}/runs/${runId}`)
    if (!res.ok) throw new Error(`Failed to get run: ${res.statusText}`)
    return res.json()
  },

  // Logs (SSE)
  streamLogs(runId: string, onMessage: (line: string) => void, onComplete: () => void) {
    const eventSource = new EventSource(`${API_BASE}/runs/${runId}/logs`)

    eventSource.onmessage = (event) => {
      const line = event.data
      if (line.startsWith('[RUN_COMPLETE:')) {
        eventSource.close()
        onComplete()
      } else {
        onMessage(line)
      }
    }

    eventSource.onerror = () => {
      eventSource.close()
      onComplete()
    }

    return () => eventSource.close()
  },

  // Vulnerabilities
  async getVulnerabilities(
    runId: string,
    filters?: { severity?: string; repo?: string; ecosystem?: string; sort?: string }
  ): Promise<Vulnerability[]> {
    const params = new URLSearchParams()
    if (filters?.severity) params.append('severity', filters.severity)
    if (filters?.repo) params.append('repo', filters.repo)
    if (filters?.ecosystem) params.append('ecosystem', filters.ecosystem)
    if (filters?.sort) params.append('sort', filters.sort)

    const res = await fetch(`${API_BASE}/runs/${runId}/vulnerabilities?${params}`)
    if (!res.ok) throw new Error(`Failed to get vulnerabilities: ${res.statusText}`)
    return res.json()
  },

  // Matrix
  async getDependencyMatrix(runId: string): Promise<DependencyMatrixRow[]> {
    const res = await fetch(`${API_BASE}/runs/${runId}/matrix/dependency`)
    if (!res.ok) throw new Error(`Failed to get dependency matrix: ${res.statusText}`)
    return res.json()
  },

  async getUpgradeMatrix(runId: string): Promise<UpgradeMatrixRow[]> {
    const res = await fetch(`${API_BASE}/runs/${runId}/matrix/upgrade`)
    if (!res.ok) throw new Error(`Failed to get upgrade matrix: ${res.statusText}`)
    return res.json()
  },

  // Reports
  async getReport(runId: string, repoName: string, filename: string): Promise<string> {
    const res = await fetch(`${API_BASE}/runs/${runId}/repos/${repoName}/reports/${filename}`)
    if (!res.ok) throw new Error(`Failed to get report: ${res.statusText}`)
    return res.text()
  },

  async getSystemReport(runId: string, filename: string): Promise<string> {
    const res = await fetch(`${API_BASE}/runs/${runId}/system-reports/${filename}`)
    if (!res.ok) throw new Error(`Failed to get system report: ${res.statusText}`)
    return res.text()
  },

  // Health
  async health(): Promise<{ status: string }> {
    const res = await fetch(`${API_BASE}/health`)
    if (!res.ok) throw new Error('Health check failed')
    return res.json()
  },
}
