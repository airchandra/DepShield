# DepShield — Screenshots & UI Mockups

Visual guide to the DepShield CLI output and web dashboard interface.

---

## CLI Usage Examples

### 1. Help Output

```bash
$ depshield --help

Usage: depshield [OPTIONS]

  DepShield — Zero-critical-vulnerabilities pipeline.

  Scan one or more git repositories for vulnerabilities across a distributed
  system, remediate dependencies to stable versions, and generate comprehensive
  documentation including SBOM, vulnerability reports, architecture diagrams,
  and upgrade matrices.

Options:
  -r, --repos PATH         Path(s) to git repositories to scan  [required]
  -o, --output PATH        Output directory for reports  [default:
                           ./depshield-output]
  --dry-run                Generate reports without applying changes (default:
                           True)
  --apply                  Apply remediation changes (requires --dry-run to be
                           False)
  -v, --verbose            Enable verbose logging
  -e, --ecosystems TEXT    Limit scanning to specific ecosystems. [default:
                           jvm, python, javascript, go, rust]
  --help                   Show this message and exit.
```

### 2. Dry-Run Scan Output

```bash
$ depshield --repos ./my-api ./my-web --output ./reports --verbose

🚀 DepShield
Repositories: ./my-api, ./my-web
Output: ./reports
Mode: DRY RUN
Ecosystems: jvm, python, javascript, go, rust

📂 Phase 1: Repository Discovery
  ✓ ./my-api (JVM: pom.xml, Python: requirements.txt)
  ✓ ./my-web (JavaScript: package.json)
  Found 2 repositories, 3 ecosystems

📦 Phase 2: SBOM Generation
  ⏳ Generating SBOM for ./my-api (JVM)... ✓
  ⏳ Generating SBOM for ./my-api (Python)... ✓
  ⏳ Generating SBOM for ./my-web (JavaScript)... ✓
  Detected 285 total dependencies

🔍 Phase 3: Vulnerability Scanning
  ⏳ Scanning ./my-api (JVM)...
    • Grype scan... ✓
    • OSV Scanner... ✓
  ⏳ Scanning ./my-api (Python)...
    • Grype scan... ✓
    • OSV Scanner... ✓
  ⏳ Scanning ./my-web (JavaScript)...
    • Grype scan... ✓
    • Trivy scan... ✓
  
  Summary:
  ├─ CRITICAL: 3
  ├─ HIGH: 7
  ├─ MEDIUM: 12
  └─ LOW: 15

📊 Phase 4: Matrix Building
  ⏳ Building dependency matrix...
  ├─ 47 unique packages
  ├─ 8 packages used in multiple repos
  └─ 2 version conflicts detected
  
  ⏳ Building upgrade matrix...
  ├─ 37 upgradeable packages
  └─ Safe versions: 29 direct, 8 transitive

⏭️  Phase 5: Remediation (SKIPPED — dry-run mode)
  No changes applied. Use: depshield ... --no-dry-run --apply

📝 Phase 6: Documentation
  ⏳ Generating system-level reports...
    • SYSTEM_ARCHITECTURE.md ✓
    • DEPENDENCY_MATRIX.md ✓
    • UPGRADE_MATRIX.md ✓
    • PIPELINE_SEQUENCE.md ✓
  
  ⏳ Generating per-repository reports...
    ./my-api:
      • SBOM.md ✓
      • VULNERABILITY_REPORT.md ✓
      • ARCHITECTURE.md ✓
      • CODING_GUIDELINES.md ✓
      • SEQUENCE_DIAGRAMS.md ✓
      • TEST_CASES.md ✓
      • UPGRADE_PLAN.md ✓
    
    ./my-web:
      • SBOM.md ✓
      • VULNERABILITY_REPORT.md ✓
      • ARCHITECTURE.md ✓
      • CODING_GUIDELINES.md ✓
      • SEQUENCE_DIAGRAMS.md ✓
      • TEST_CASES.md ✓
      • UPGRADE_PLAN.md ✓

✅ Pipeline completed successfully
Reports available at: ./reports
```

### 3. Applying Remediations

```bash
$ depshield --repos ./my-api ./my-web --output ./reports --no-dry-run --apply

🚀 DepShield
Repositories: ./my-api, ./my-web
Output: ./reports
Mode: APPLY
Ecosystems: jvm, python, javascript, go, rust

📂 Phase 1-3: [Discovery, SBOM, Scanning — same as above] ✓

📊 Phase 4: Matrix Building ✓

⏳ Phase 5: Remediation (APPLY MODE)
  
  ./my-api (JVM ecosystem):
    📦 Git stash (backup)... ✓
    🔷 Running OpenRewrite recipes...
      • Upgrading spring-boot 5.1.0 → 6.0.0... ✓
      • Upgrading log4j 2.17.0 → 2.18.1... ✓
    🔨 Building (mvn clean install)...
      [INFO] BUILD SUCCESS ✓
    ✅ Running tests (mvn test)...
      [INFO] Tests run: 142, Failures: 0, Skipped: 0 ✓
    📝 Committing changes... ✓
  
  ./my-api (Python ecosystem):
    📦 Git stash (backup)... ✓
    🐍 Running pip-audit --fix...
      • Upgrading requests 2.28.0 → 2.31.0... ✓
      • Upgrading urllib3 1.26.11 → 2.0.0... ✓
    🔨 Building (pytest)...
      ===== 87 passed in 2.34s ===== ✓
    📝 Committing changes... ✓
  
  ./my-web (JavaScript ecosystem):
    📦 Git stash (backup)... ✓
    📦 Running npm audit fix...
      • Upgraded next 13.0.0 → 14.0.0... ✓
      • Upgraded react 18.1.0 → 18.2.0... ✓
    🔨 Building (npm test)...
      ✓ 234 tests passed ✓
    📝 Committing changes... ✓

✅ Remediation Complete
  ├─ 3 repos processed
  ├─ 6 ecosystem upgrades successful
  └─ 0 rollbacks

📝 Phase 6: Documentation
  [Same as dry-run] ✓

✅ Pipeline completed successfully
Reports available at: ./reports
```

---

## Web Dashboard Screenshots

### Dashboard Layout Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DepShield Dashboard                         🔍 Search runs          ⚙️ Settings  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────┐  ┌──────────────────────────────────┐ │
│  │  NEW SCAN                       │  │  RECENT RUNS                     │ │
│  │                                 │  │                                  │ │
│  │ Repositories (one per line):    │  │ ┌────────────────────────────┐  │ │
│  │ ┌─────────────────────────────┐ │  │ │ Run #1 (3h ago)            │  │ │
│  │ │./repos/api                  │ │  │ │ Status: ✅ DONE             │  │ │
│  │ │./repos/web                  │ │  │ │ Repos: 2 | Vulns: 12       │  │ │
│  │ │./repos/worker               │ │  │ │ 🔷 JVM 🐍 Python           │  │ │
│  │ └─────────────────────────────┘ │  │ └────────────────────────────┘  │ │
│  │                                 │  │ ┌────────────────────────────┐  │ │
│  │ Mode:                           │  │ │ Run #2 (1d ago)            │  │ │
│  │ ⦿ Dry Run    ○ Apply            │  │ │ Status: ✅ DONE             │  │ │
│  │                                 │  │ │ Repos: 3 | Vulns: 28       │  │ │
│  │ Ecosystems:                     │  │ │ 🔷 JVM 🐍 Python 📦 Node   │  │ │
│  │ ☑ JVM  ☑ Python  ☑ Node        │  │ └────────────────────────────┘  │ │
│  │ ☑ Go   ☑ Rust                  │  │ ┌────────────────────────────┐  │ │
│  │                                 │  │ │ Run #3 (3d ago)            │  │ │
│  │ ┌─────────────────────────────┐ │  │ │ Status: ⏳ RUNNING           │  │ │
│  │ │     START SCAN              │ │  │ │ Repos: 2 | Vulns: 5        │  │ │
│  │ └─────────────────────────────┘ │  │ │ 🐹 Go                      │  │ │
│  │                                 │  │ └────────────────────────────┘  │ │
│  └─────────────────────────────────┘  │                                  │ │
│                                        └──────────────────────────────────┘ │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Run Details Page — Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DepShield > Run #1                    [Share]  [Export]  [Refresh]  [←Back] │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Status: ✅ DONE (completed 2h 14m 37s)  Started: Oct 28, 2024 3:45:22 PM │
│                                                                               │
│  Summary Cards                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Repos        │  │ Dependencies │  │ Vulnerabilty │  │ Status       │    │
│  │ 2            │  │ 285          │  │ CRITICAL: 3  │  │ Build: ✅    │    │
│  │ Scanned      │  │ Detected     │  │ HIGH: 7      │  │ Tests: ✅    │    │
│  │              │  │              │  │ MEDIUM: 12   │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                                               │
│  Per-Repository Status                                                        │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ ▼ ./my-api                                                [3 docs]  │ │
│  │   Ecosystems:  🔷 JVM  🐍 Python                                    │ │
│  │   Dependencies: 145  Build: ✅  Tests: ✅  Lint: ✅                │ │
│  │   Vulnerabilities: CRITICAL:1  HIGH:3  MEDIUM:4  LOW:3            │ │
│  │   Status: ✅ Remediation successful (2 packages upgraded)         │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ ▼ ./my-web                                                [3 docs]  │ │
│  │   Ecosystems:  📦 Node                                              │ │
│  │   Dependencies: 140  Build: ✅  Tests: ✅  Lint: ⚠️ (12 issues)   │ │
│  │   Vulnerabilities: CRITICAL:2  HIGH:4  MEDIUM:8  LOW:12           │ │
│  │   Status: ✅ Remediation successful (4 packages upgraded)         │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  📊 Live Scan Log (auto-scroll)                                               │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 14:47:22 [INFO] Phase 1: Repository Discovery                        │ │
│  │ 14:47:22 [INFO] ✓ ./my-api (JVM: pom.xml, Python: requirements.txt) │ │
│  │ 14:47:23 [INFO] ✓ ./my-web (Node: package.json)                     │ │
│  │ 14:47:24 [INFO] Phase 2: SBOM Generation                             │ │
│  │ 14:47:24 [INFO] ⏳ Generating SBOM for ./my-api (JVM)...            │ │
│  │ 14:47:38 [INFO] ✓ SBOM generated (145 dependencies)                 │ │
│  │ 14:47:39 [INFO] ⏳ Generating SBOM for ./my-api (Python)...         │ │
│  │ 14:47:52 [INFO] ✓ SBOM generated (78 dependencies)                  │ │
│  │ ... [continued] ...                                                  │ │
│  │ 14:50:12 [INFO] Phase 6: Documentation Complete                     │ │
│  │ 14:50:12 [INFO] ✅ Pipeline completed successfully                  │ │
│  │                                                                       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  Tabs:  Overview  [Vulnerabilities]  [Matrices]  [Reports]                 │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Vulnerabilities Tab — Filterable Table

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DepShield > Run #1 > Vulnerabilities                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Filters: [Severity ▼] [Repo ▼] [Ecosystem ▼] [Search...]                 │
│           [CRITICAL] [HIGH] [MEDIUM] [LOW]  [Apply Filters] [Clear]       │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ CVE ID          │ Package        │ Repo    │ Sev.  │ CVSS │ Current   ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ CVE-2024-1234   │ spring-boot    │ ./my-api│ 🔴 CR │ 9.8  │ 5.1.0 → 6.0││
│  │ CVE-2024-5678   │ log4j          │ ./my-api│ 🔴 CR │ 9.2  │ 2.17.0 → ││
│  │ CVE-2024-9012   │ urllib3        │ ./my-api│ 🟠 HI │ 7.5  │ 1.26.11→ ││
│  │ CVE-2024-3456   │ requests       │ ./my-api│ 🟠 HI │ 6.8  │ 2.28.0→ ││
│  │ CVE-2024-7890   │ django         │ ./my-api│ 🟠 HI │ 7.1  │ 3.2.0→ ││
│  │ CVE-2024-2345   │ next.js        │ ./my-web│ 🔴 CR │ 8.9  │ 13.0.0→ ││
│  │ CVE-2024-6789   │ react          │ ./my-web│ 🟠 HI │ 5.2  │ 18.1.0→ ││
│  │ CVE-2024-0123   │ webpack        │ ./my-web│ 🟡 ME │ 5.4  │ 5.88.0→ ││
│  │ CVE-2024-4567   │ lodash         │ ./my-web│ 🟡 ME │ 4.9  │ 4.17.21→││
│  │ CVE-2024-8901   │ dotenv         │ ./my-web│ 🟦 LO │ 2.1  │ 8.6.0→ ││
│  │                                                                         ││
│  │  Showing 1-10 of 22 vulnerabilities            [Next 10] [View All]   ││
│  │                                                                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                               │
│  Click on CVE ID for details → External advisory link & recommendations     │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Matrices Tab — Dependency & Upgrade Tables

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DepShield > Run #1 > Matrices                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  [Dependency Matrix]  [Upgrade Matrix]                                      │
│                                                                               │
│  DEPENDENCY MATRIX                                                            │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ Package          │ Repos               │ Versions      │ Status        ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ spring-boot      │ ./my-api            │ 5.1.0         │ Single        ││
│  │ log4j            │ ./my-api            │ 2.17.0        │ Single        ││
│  │ commons-lang3    │ ./my-api            │ 3.12.0        │ Single        ││
│  │ requests         │ ./my-api            │ 2.28.0        │ Single        ││
│  │ urllib3          │ ./my-api, transitive│ 1.26.11       │ Shared        ││
│  │ next.js          │ ./my-web            │ 13.0.0        │ Single        ││
│  │ react            │ ./my-web            │ 18.1.0        │ Single        ││
│  │ webpack          │ ./my-web            │ 5.88.0        │ Single        ││
│  │ typescript       │ ./my-web            │ 5.0.0         │ Single        ││
│  │ lodash           │ ./my-web            │ 4.17.21       │ ⚠️ Conflict    ││
│  │                                                                         ││
│  │  47 unique packages | 8 shared | 2 conflicts detected                 ││
│  │                                                                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                               │
│  UPGRADE MATRIX                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ Package     │ Current   │ Safe Version │ Severity │ CVSS │ CVEs Fixed ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ spring-boot │ 5.1.0     │ 6.0.0        │ 🔴 CR    │ 9.8  │ 1         ││
│  │ log4j       │ 2.17.0    │ 2.18.1       │ 🔴 CR    │ 9.2  │ 1         ││
│  │ requests    │ 2.28.0    │ 2.31.0       │ 🟠 HI    │ 6.8  │ 1         ││
│  │ urllib3     │ 1.26.11   │ 2.0.0        │ 🟠 HI    │ 7.5  │ 2         ││
│  │ next.js     │ 13.0.0    │ 14.0.0       │ 🔴 CR    │ 8.9  │ 1         ││
│  │ react       │ 18.1.0    │ 18.2.0       │ 🟠 HI    │ 5.2  │ 1         ││
│  │ webpack     │ 5.88.0    │ 5.90.0       │ 🟡 ME    │ 5.4  │ 1         ││
│  │ dotenv      │ 8.6.0     │ 16.0.0       │ 🟦 LO    │ 2.1  │ 1         ││
│  │                                                                         ││
│  │ 37 upgradeable packages | 29 direct | 8 transitive                    ││
│  │                                                                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                               │
│  Click package name to see details, pull requests, and migration guides     │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Reports Tab — Documentation Viewer

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DepShield > Run #1 > ./my-api > Reports                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Reports:                                                                     │
│  [📄 SBOM] [🚨 Vulnerabilities] [🏗️ Architecture] [📋 Guidelines]            │
│  [📊 Sequences] [🧪 Test Cases] [📈 Upgrade Plan]                          │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────────┐│
│  │ VULNERABILITY REPORT                                                     ││
│  │ ════════════════════════════════════════════════════════════════════════ ││
│  │                                                                          ││
│  │ ## Vulnerability Report: ./my-api                                      ││
│  │                                                                          ││
│  │ **Generated:** Oct 28, 2024 3:45:22 PM                                 ││
│  │ **Ecosystems:** JVM (Maven 3.8.1), Python (pip 21.0.1)               ││
│  │ **Dependencies:** 223 total                                            ││
│  │                                                                          ││
│  │ ### Summary                                                            ││
│  │                                                                          ││
│  │ | Severity | Count | Status           |                               ││
│  │ |----------|-------|------------------|                               ││
│  │ | CRITICAL | 1     | ❌ Remediate     |                               ││
│  │ | HIGH     | 3     | ✅ Remediated    |                               ││
│  │ | MEDIUM   | 4     | ✅ Remediated    |                               ││
│  │ | LOW      | 3     | ⚠️ Review        |                               ││
│  │                                                                          ││
│  │ ### Critical Vulnerabilities                                           ││
│  │                                                                          ││
│  │ #### CVE-2024-1234: Spring Boot RCE                                   ││
│  │                                                                          ││
│  │ - **Package:** spring-boot-autoconfigure                              ││
│  │ - **Current Version:** 5.1.0                                          ││
│  │ - **Safe Version:** 6.0.0                                             ││
│  │ - **CVSS Score:** 9.8 (Critical)                                      ││
│  │ - **Description:** Remote code execution in Spring Boot actuator...   ││
│  │ - **Advisory:** [NVD Link]                                            ││
│  │ - **Remediation:** Upgrade to 6.0.0 (breaking change)                ││
│  │ - **Status:** ✅ Fixed in run                                         ││
│  │                                                                          ││
│  │ ... [more vulnerabilities] ...                                         ││
│  │                                                                          ││
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                                                               │
│  [Scroll for more] [Print] [Download MD] [Download PDF]                    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Architecture Diagram in Report

```
Rendered Mermaid C4 Context Diagram:

┌─────────────────────────────────────────────────────────────┐
│                     System Context                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ┌────────────────┐                      │
│                    │   End Users    │                      │
│                    │   (Dev Team)   │                      │
│                    └────────┬───────┘                      │
│                             │                              │
│                             │ uses                         │
│                             ▼                              │
│                    ┌────────────────┐                      │
│                    │   My API Svc   │                      │
│                    │ (Spring Boot)  │                      │
│                    │  [JVM]         │                      │
│                    └────────────────┘                      │
│                             │                              │
│                             │ depends on                   │
│                             ▼                              │
│    ┌───────────────────────────────────────────────────┐  │
│    │  External Libraries                               │  │
│    │  ├─ spring-boot v5.1.0 (CRITICAL)                │  │
│    │  ├─ log4j v2.17.0 (CRITICAL)                     │  │
│    │  ├─ commons-lang3 v3.12.0                        │  │
│    │  ├─ jackson v2.14.0                              │  │
│    │  └─ ... 140+ more dependencies                   │  │
│    └───────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Rendered Mermaid Sequence Diagram (Remediation Flow):

participant User
participant Pipeline
participant Git
participant Build
participant TestRunner

User->>Pipeline: trigger remediation
Pipeline->>Git: git stash (backup)
Git-->>Pipeline: ✓ stashed
Pipeline->>Pipeline: run OpenRewrite
Pipeline->>Build: mvn clean install
Build-->>Pipeline: ✓ success
Pipeline->>TestRunner: mvn test
TestRunner-->>Pipeline: ✓ all tests pass
Pipeline->>Git: git add + commit
Git-->>Pipeline: ✓ committed
Pipeline-->>User: ✓ complete

[Shows as professionally rendered Mermaid diagram]
```

---

## Dark Mode Variant

All screenshots have full dark mode support:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DepShield Dashboard      [🌙 Dark]                      ⚙️ Settings  │
├─────────────────────────────────────────────────────────────────────────────┤
│ [Dark background] [Light text] [Colored severity indicators remain bright]   │
│                                                                               │
│ Cards and tables styled for dark readability with proper contrast ratios     │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Mobile Responsive Layout

Dashboard adapts to mobile screens (< 768px):

```
┌──────────────────────┐
│ DepShield    ☰      │  ← Hamburger menu
├──────────────────────┤
│                      │
│  📝 NEW SCAN         │
│  ┌────────────────┐  │
│  │ ./repos...     │  │
│  └────────────────┘  │
│  [Dry Run] [Apply]   │
│  ☑ JVM ☑ Python     │
│  [START SCAN]        │
│                      │
│  ═════════════════  │
│                      │
│  📊 RECENT RUNS      │
│  ┌────────────────┐  │
│  │ Run #1 ✅      │  │
│  │ 2 repos, 12 CVE│  │
│  └────────────────┘  │
│  ┌────────────────┐  │
│  │ Run #2 ✅      │  │
│  │ 3 repos, 28 CVE│  │
│  └────────────────┘  │
│                      │
└──────────────────────┘
```

---

## Real-Time Features

### Live Log Streaming (SSE)

Logs stream in real-time as the scan executes:

```
14:47:22 [INFO] Phase 1: Repository Discovery
14:47:22 [INFO] ✓ ./my-api (JVM: pom.xml, Python: requirements.txt)
14:47:23 [INFO] ✓ ./my-web (Node: package.json)
14:47:24 [INFO] Phase 2: SBOM Generation
14:47:24 [INFO] ⏳ Generating SBOM for ./my-api (JVM)...
  [Stream pauses while tool runs]
14:47:38 [INFO] ✓ SBOM generated (145 dependencies)
  [Next line appears immediately when available]
14:47:39 [INFO] ⏳ Generating SBOM for ./my-api (Python)...
```

### Auto-Refresh

Summary cards and vulnerability counts update in real-time:

```
│ CRITICAL: 3    │    │ CRITICAL: 3    │    │ CRITICAL: 5    │
│ HIGH: 7        │ → │ HIGH: 7        │ → │ HIGH: 8        │
│ MEDIUM: 12     │    │ MEDIUM: 14     │    │ MEDIUM: 16     │
│ LOW: 15        │    │ LOW: 15        │    │ LOW: 15        │
```

---

## Export Formats

Users can export reports in multiple formats:

```
[Download as:]
├─ 📄 Markdown (.md)      — Plain text with diagrams
├─ 📊 JSON (.json)        — Structured data for parsing
├─ 📈 CSV (.csv)          — Spreadsheet-friendly vulnerabilities
└─ 📑 PDF (.pdf)          — Professional printable format
```

---

## Accessibility Features

- ✅ WCAG 2.1 AA compliant
- ✅ Keyboard navigation (Tab, Enter, Arrow keys)
- ✅ Screen reader support (ARIA labels)
- ✅ High contrast mode
- ✅ Dark mode support
- ✅ Respects `prefers-reduced-motion`

---

## Summary

The DepShield interface provides:

1. **CLI** — Professional command-line output with progress indicators and rich formatting
2. **Dashboard** — Intuitive web UI for monitoring, exploring, and managing scans
3. **Reports** — Professional markdown documentation with embedded diagrams
4. **Real-Time Features** — Live log streaming, auto-updating status cards
5. **Responsive Design** — Works on desktop, tablet, and mobile
6. **Accessibility** — Full keyboard and screen reader support
7. **Export Options** — Multiple formats for integration with other tools

All visual elements follow professional design standards with consistent color coding, clear typography, and thoughtful UX patterns.
