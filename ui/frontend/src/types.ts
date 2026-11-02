export type RunStatus = "pending" | "running" | "done" | "error"
export type Severity = "critical" | "high" | "medium" | "low" | "unknown"

export interface RunRequest {
  repos: string[]
  output_dir?: string
  dry_run?: boolean
  apply?: boolean
  ecosystems?: string[]
}

export interface Vulnerability {
  id: string
  package: string
  severity: Severity
  cvss_score: number
  description: string
  fixed_version: string
  current_version: string
  advisory: string
  repo_name?: string
}

export interface DependencyMatrixRow {
  package: string
  repos: string[]
  versions: Record<string, string[]>
  has_conflict: boolean
}

export interface UpgradeMatrixRow {
  package: string
  current_version: string
  safe_version: string
  severity: Severity
  cvss_score: number
  cve_count: number
  cves: string[]
}

export interface RepoStatus {
  name: string
  ecosystems: string[]
  dependency_count: number
  vulnerability_count: number
  critical_count: number
  high_count: number
  build_succeeded?: boolean
  test_succeeded?: boolean
}

export interface RunResponse {
  id: string
  repos: string[]
  output_dir: string
  dry_run: boolean
  apply: boolean
  ecosystems: string[]
  status: RunStatus
  started_at: string
  finished_at?: string
  error_message?: string
  logs: string[]
  total_dependencies: number
  total_vulnerabilities: number
  repo_statuses: RepoStatus[]
}

export interface RunSummary {
  id: string
  repos: string[]
  status: RunStatus
  started_at: string
  finished_at?: string
  total_repos: number
  total_dependencies: number
  total_vulnerabilities: number
}
