# DepShield Specification

## 1. Functional Specifications

### 1.1 Core Functionality

#### Discovery Phase
DepShield must automatically detect and catalog repositories:

**Input**: List of repository paths (local or remote)
**Process**:
- Validate git repositories
- Detect ecosystem (presence of manifest files: pom.xml, package.json, go.mod, Cargo.toml, pyproject.toml)
- Extract build commands (mvn, npm, go build, cargo build, python setup.py)
- Extract test commands (mvn test, npm test, go test, cargo test, pytest)
- Extract lint commands (checkstyle, eslint, golangci-lint, cargo clippy)

**Output**: 
```python
RepoManifest(
    path: Path,
    name: str,
    ecosystems: list[Ecosystem],
    build_command: str,
    test_command: str,
    lint_command: str,
    dependencies: list[Dependency]
)
```

**Requirements**:
- Must work with git and non-git directories (but prefer git for safety)
- Detect multiple ecosystems per repo (e.g., Python backend + JavaScript frontend)
- Fail gracefully if a repo doesn't have manifest files

#### SBOM Generation
DepShield must generate Software Bill of Materials for each repository:

**Tool**: Syft
**Output Format**: CycloneDX JSON
**Contents**:
- Component name, version, license
- Source/package manager
- Dependency relationships

**Requirements**:
- Generate CycloneDX JSON (not SPDX or custom format)
- Preserve full component information
- Support all 5 ecosystems

#### Vulnerability Scanning
DepShield must identify vulnerabilities in dependencies:

**Primary Scanner**: Grype (consumes SBOM)
**Secondary Scanners**: 
- OSV Scanner (Google's vulnerability DB cross-check)
- Trivy (filesystem + container scanning)

**Detection Scope**:
- Direct dependencies
- Transitive dependencies
- Unresolved dependencies (dependencies not yet installed)

**Output**:
```python
Vulnerability(
    id: str,           # CVE-XXXX-XXXXX or GHSA-XXXX-XXXX-XXXX
    package: str,
    severity: Severity,  # critical, high, medium, low, unknown
    cvss_score: float,
    description: str,
    fixed_version: str,
    current_version: str,
    advisory: str      # URL or source info
)
```

**Requirements**:
- Deduplicate CVE IDs across scanners
- Support all severity levels
- Include CVSS 3.0+ scores
- Link to official advisories

#### Dependency Analysis
DepShield must build a unified view of dependencies across repos:

**Dependency Matrix**:
- Input: All dependencies from all repos
- Output: Table showing which packages are in which repos at which versions
- Identify version conflicts (same package at different versions)
- Identify shared dependencies (same package in multiple repos)

**Upgrade Matrix**:
- Input: All vulnerabilities across repos
- Process: For each CVE, find the safe version that fixes it
- Output: Recommended upgrades per package

**Requirements**:
- Identify all version conflicts
- Recommend conservative upgrades (don't jump major versions without reason)
- Flag packages that have no safe upgrade yet

#### Remediation
DepShield must safely upgrade vulnerable dependencies:

**Execution Model**:
- Per-repo sequential (don't parallelize upgrades in same repo due to lock file conflicts)
- Cross-repo parallel (different repos can upgrade simultaneously)
- Dry-run first (default: no mutations)
- Explicit approval required for apply mode

**Ecosystem-Specific Tools**:
| Ecosystem | Tool | Command |
|-----------|------|---------|
| JVM | OpenRewrite | mvn openrewrite:run / ./gradlew rewriteRun |
| Python | pip-audit | pip-audit --fix |
| JavaScript | npm audit | npm audit fix --force |
| Go | govulncheck | go get -u |
| Rust | cargo-audit | cargo update |

**Safety Mechanisms**:
1. Git stash before any mutations
2. Build validation (run build command post-upgrade)
3. Test validation (run test command post-upgrade)
4. Auto-rollback if build or tests fail (git stash pop)
5. Human approval (--no-dry-run --apply required)

**Requirements**:
- Never break the build
- Rollback fully if anything fails
- Report what changed and why
- Support partial failures (some packages upgraded, others skipped)

#### Documentation Generation
DepShield must produce 11 markdown files per run:

**Per-Repository Documents** (in `<repo>/docs/`):
1. **SBOM.md** - Component list, licenses, vulnerability summary
2. **VULNERABILITY_REPORT.md** - Detailed CVE list with severity, CVSS, descriptions
3. **UPGRADE_PLAN.md** - Specific upgrades needed with before/after versions
4. **ARCHITECTURE.md** - C4 component diagram (Mermaid)
5. **CODING_GUIDELINES.md** - Detected coding standards and conventions
6. **SEQUENCE_DIAGRAMS.md** - Remediation flow diagram (Mermaid flowchart)
7. **TEST_CASES.md** - Testing strategy and test matrix

**System-Level Documents** (in output directory):
8. **SYSTEM_ARCHITECTURE.md** - Full C4 context diagram with inter-repo relationships
9. **DEPENDENCY_MATRIX.md** - Table of cross-repo dependency usage
10. **UPGRADE_MATRIX.md** - Global upgrade recommendations
11. **PIPELINE_SEQUENCE.md** - End-to-end execution sequence diagram (Mermaid)

**Diagram Requirements**:
- All diagrams use Mermaid syntax
- C4 diagrams: context, components, deployment views
- Sequence diagrams: show scanner/remediator/reporter flow
- Flowcharts: remediation decision tree
- Quality: publication-ready (clear, labeled, color-coded by severity)

**Requirements**:
- All output is valid Markdown
- Diagrams are embedded (not external images)
- Documents are self-contained and complete
- Severity colors: critical=red, high=orange, medium=yellow, low=blue, unknown=gray

### 1.2 API Specifications

#### REST API Endpoints

**Runs Management**
```
POST /api/runs
  Input: { repos: [], dry_run: bool, apply: bool, ecosystems: [] }
  Output: { id: string }
  Purpose: Create and start a new scan

GET /api/runs
  Output: [{ id, repos, status, started_at, total_deps, total_vulns }]
  Purpose: List all past scans

GET /api/runs/{id}
  Output: { all run data + logs + results }
  Purpose: Get full run details
```

**Vulnerabilities**
```
GET /api/runs/{id}/vulnerabilities?severity=critical&sort=cvss_score
  Output: Vulnerability[]
  Purpose: Query vulnerabilities with filtering
```

**Matrices**
```
GET /api/runs/{id}/matrix/dependency
  Output: [{ package, repos, versions, has_conflict }]
  Purpose: Cross-repo dependency analysis

GET /api/runs/{id}/matrix/upgrade
  Output: [{ package, current, safe_version, severity, cvss, cves }]
  Purpose: Upgrade recommendations
```

**Logs**
```
GET /api/runs/{id}/logs (SSE)
  Output: Server-Sent Events stream
  Purpose: Real-time log streaming
```

**Reports**
```
GET /api/runs/{id}/repos/{name}/reports/{filename}
  Output: Markdown text
  Purpose: Serve generated markdown files

GET /api/runs/{id}/system-reports/{filename}
  Output: Markdown text
  Purpose: Serve system-level reports
```

#### Data Models

```typescript
// Core models
interface Vulnerability {
  id: string
  package: string
  severity: "critical" | "high" | "medium" | "low" | "unknown"
  cvss_score: number
  description: string
  fixed_version: string
  current_version: string
  advisory: string
}

interface Dependency {
  name: string
  version: string
  ecosystem: Ecosystem
  license: string
  vulnerabilities: Vulnerability[]
}

interface RepoManifest {
  path: string
  name: string
  ecosystems: Ecosystem[]
  dependencies: Dependency[]
  build_command?: string
  test_command?: string
  lint_command?: string
}

interface ScanResult {
  repo: RepoManifest
  sbom_path: string
  vulnerabilities: Vulnerability[]
  success: boolean
  error?: string
}

interface RemediationResult {
  repo: RepoManifest
  upgraded_dependencies: { [pkg]: [old_ver, new_ver] }
  recipes_applied: string[]
  build_succeeded: boolean
  test_succeeded: boolean
  success: boolean
  error?: string
}

interface RunState {
  id: string
  repos: string[]
  status: "pending" | "running" | "done" | "error"
  started_at: datetime
  finished_at?: datetime
  logs: string[]
  scan_results: ScanResult[]
  remediation_results: RemediationResult[]
  dep_matrix: object
  upgrade_matrix: object
}
```

### 1.3 CLI Specifications

#### Command Syntax

```bash
depshield [OPTIONS]

Options:
  --repos, -r PATH (required, multiple)
    List of repository paths to scan
  
  --output, -o PATH (default: ./depshield-output)
    Output directory for reports
  
  --dry-run (default: true)
    Generate reports without applying changes
  
  --apply (default: false)
    Apply remediations (requires --no-dry-run)
  
  --verbose, -v (default: false)
    Enable debug logging
  
  --ecosystems, -e (default: all)
    Limit to specific ecosystems: jvm, python, javascript, go, rust
```

#### Example Invocations

```bash
# Scan only (safe, read-only)
depshield --repos ./api ./frontend --dry-run --verbose

# Apply remediations (requires explicit approval)
depshield --repos ./api --no-dry-run --apply --verbose

# Specific ecosystems
depshield --repos ./project --ecosystems jvm python

# Custom output
depshield --repos . --output ./security-audit
```

## 2. Technical Specifications

### 2.1 Architecture

**6-Phase Pipeline**:
```
Phase 1: Discovery
  └─ Detect repos, ecosystems, build commands

Phase 2: SBOM Generation
  └─ Syft → CycloneDX JSON per repo

Phase 3: Vulnerability Scanning
  └─ Grype + OSV + Trivy → deduplicated CVEs

Phase 4: Matrix Building
  └─ Dependency matrix + Upgrade matrix

Phase 5: Remediation (optional, if --apply)
  └─ Ecosystem-specific upgrades with build validation

Phase 6: Documentation
  └─ Generate 11 markdown files per run
```

### 2.2 Concurrency Model

**Scanning** (parallel across repos):
- SBOM generation: 4 repos in parallel
- Vulnerability scanning: 4 repos in parallel
- Cross-checks: Sequential after scanning (deduplication)

**Remediation** (sequential within repo, parallel across repos):
- Per-repo remediation is sequential (lock file conflicts)
- Multiple repos can remediate in parallel
- No more than 2 concurrent remediations (resource limits)

### 2.3 Error Handling

**Non-Fatal Errors** (continue with next phase):
- Syft fails to generate SBOM → skip that repo, log warning
- Grype returns no results → assume clean, continue
- Test command fails → log failure, continue to next phase

**Fatal Errors** (stop entire pipeline):
- No repositories found → exit with error code 1
- Invalid repo paths → exit with error code 1
- Disk space exhausted → exit with error code 1

**Remediation Errors** (auto-rollback):
- Build fails post-upgrade → git stash pop, flag package as failed
- Tests fail post-upgrade → git stash pop, flag package as failed
- Upgrade breaks API contract → rollback, mark for manual review

### 2.4 Performance Targets

- Discover 10 repos: < 5 seconds
- Scan 10 repos: < 2 minutes (network dependent)
- Build matrices: < 10 seconds
- Remediate 10 repos: < 5 minutes (build/test dependent)
- Generate docs: < 10 seconds

**Total time for 10 repos**: ~8 minutes (network + build time)

### 2.5 Storage Requirements

- SBOM per repo: ~1-10 MB (depends on dependency count)
- Vulnerability data: ~1-50 KB per CVE
- Reports per run: ~5-50 MB (depends on vuln count)
- Logs per run: ~1-10 MB

**Typical disk usage per run**: ~100-500 MB for 10 repos

## 3. Integration Specifications

### 3.1 Docker Integration

**Dockerfile Requirements**:
- Base: python:3.12-slim
- Installed tools: syft, grype, osv-scanner, trivy, mvn, npm, go, cargo
- Entry point: depshield CLI
- Volume mounts: /repos (input), /output (results)

**Docker Compose**:
- Services: harness (main service)
- Volumes: repo path, output path
- Network: bridge
- Resource limits: none (user-configurable)

### 3.2 CI/CD Integration

**GitHub Actions**:
- Workflow: .github/workflows/depshield.yml
- Trigger: push to main, PR, manual dispatch, schedule (daily)
- Artifacts: upload reports to artifact storage
- Notifications: PR comments with summary

**GitLab CI**:
- Pipeline: .gitlab-ci.yml with stages (scan, remediate, report)
- Artifacts: upload to artifact repository
- Reports: generate SAST report in GitLab format

### 3.3 External Tool Integration

**Required Tools** (bundled in Docker):
- Syft (SBOM generation)
- Grype (vulnerability scanning)
- osv-scanner (vulnerability cross-check)
- Trivy (filesystem scanning)

**Language Tools** (assumed available):
- Maven/Gradle (JVM)
- pip/poetry (Python)
- npm/yarn (JavaScript)
- go (Go)
- cargo (Rust)

**Optional Tools** (nice to have):
- pre-commit framework (local hook integration)
- husky (git hooks)

## 4. Data Specifications

### 4.1 Input Data Format

**Repository List**:
- File paths (local): ./api, ./frontend, /absolute/path/to/repo
- Git URLs: git@github.com:org/repo.git, https://github.com/org/repo.git
- One per line in config file or CLI

**Configuration File** (optional YAML):
```yaml
repos:
  - ./api
  - ./frontend
  - ./services/data
output_dir: ./security-audit
dry_run: true
ecosystems:
  - jvm
  - python
  - javascript
```

### 4.2 Output Data Format

**SBOM Format**: CycloneDX XML/JSON (standard)
**Vulnerability Format**: JSON with CVE fields
**Reports Format**: Markdown with embedded Mermaid diagrams
**Logs Format**: Plain text, timestamped

### 4.3 Data Retention

**By Default**:
- Results: Kept indefinitely in output directory
- Logs: Kept in run record (in-memory or DB)
- SBOM files: Kept in ./depshield-output/sbom/

**Cleanup**:
- Old runs: Users responsible (can be automated via cron)
- Temporary files: Cleaned up after each phase
- Git stashes: Cleaned up after remediation succeeds or fails

## 5. Security Specifications

### 5.1 Safety Guarantees

**No Code Execution**:
- Scanning doesn't execute any code (static analysis only)
- Remediation only modifies manifest files, no script execution

**No Data Exfiltration**:
- All operations are local (no cloud upload)
- No credentials or secrets logged
- No telemetry or analytics

**Reversibility**:
- All mutations can be reverted (git stash)
- Original state recoverable (git checkout)
- Build failures trigger automatic rollback

### 5.2 Credential Handling

**Requirement**:
- Never log or display credentials, API keys, passwords
- Strip sensitive environment variables from logs
- Use git credential helpers for private repos

### 5.3 Vulnerability in DepShield Itself

**Handling**:
- Security patches released immediately
- Vulnerabilities in dependencies handled within 24 hours
- CVE disclosure follow responsible disclosure practices

## 6. Compatibility Specifications

### 6.1 Ecosystem Compatibility Matrix

| Ecosystem | SBOM | Scan | Remediate | Auto-detect | Notes |
|-----------|------|------|-----------|-------------|-------|
| JVM | ✅ | ✅ | ✅ | ✅ | Maven + Gradle |
| Python | ✅ | ✅ | ✅ | ✅ | pip, poetry, conda |
| JavaScript | ✅ | ✅ | ✅ | ✅ | npm, yarn, pnpm |
| Go | ✅ | ✅ | ✅ | ✅ | go.mod |
| Rust | ✅ | ✅ | ✅ | ✅ | Cargo.toml |

### 6.2 Platform Support

| Platform | CLI | Docker | CI/CD |
|----------|-----|--------|-------|
| Linux | ✅ | ✅ | ✅ |
| macOS | ✅ | ✅ | ✅ |
| Windows | ✅ | ✅ (WSL) | ✅ |

### 6.3 Python Version Support

- **Minimum**: Python 3.11
- **Recommended**: Python 3.12+
- **Support Duration**: Until Python EOL

## 7. Versioning & Deprecation

### 7.1 Semantic Versioning

- MAJOR: Breaking changes (API, CLI, output format)
- MINOR: New features, backward-compatible
- PATCH: Bug fixes, security patches

### 7.2 Deprecation Policy

- Features deprecated with 6-month notice
- Removal only in major version bump
- Changelog documents all breaking changes

## Conclusion

DepShield is a comprehensive vulnerability management system for distributed systems. This specification defines the complete functional and technical scope, ensuring consistency across all components and enabling future development with clear boundaries.
