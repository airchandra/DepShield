# DepShield Architecture Diagrams

**⭐ Draw.io Specifications Available!**

Professional specifications for creating diagrams in Draw.io: **[ARCHITECTURE_DIAGRAMS.md](./ARCHITECTURE_DIAGRAMS.md)**

Includes detailed specs for 7 diagrams with dimensions, colors, components, and layout guides.

Below are Mermaid-based versions of the key diagrams. For professional draw.io versions, see the specification document.

---

## 1. C4 Context Diagram — System Scope

High-level view of DepShield as a black box and its interaction with the world.

```mermaid
graph TB
    User["👤 User<br/>(Security/DevOps Engineer)"]
    CLI["Command Line<br/>Interface"]
    Dashboard["Web Dashboard<br/>(FastAPI + React)"]
    Repos["Git Repositories<br/>(Multi-ecosystem)"]
    GitHub["GitHub<br/>(Source Control)"]
    
    User -->|"Commands"| CLI
    User -->|"Browser"| Dashboard
    User -->|"Triggers"| Dashboard
    
    CLI -->|"Scans & Remediates"| Repos
    Dashboard -->|"Orchestrates"| CLI
    
    Repos -->|"Push"| GitHub
    Dashboard -->|"View Results"| Repos
    
    style User fill:#e1f5ff
    style CLI fill:#fff3e0
    style Dashboard fill:#f3e5f5
    style Repos fill:#e8f5e9
    style GitHub fill:#fce4ec
```

---

## 2. C4 Container Diagram — System Components

Decomposed view showing major containers and communication paths.

```mermaid
graph TB
    User["👤 User"]
    
    subgraph "DepShield System"
        CLI["🖥️ CLI<br/>Click Application<br/>(Python)"]
        Core["🔧 Core Pipeline<br/>Orchestration<br/>(Python)"]
        Backend["⚙️ FastAPI Backend<br/>REST + SSE<br/>(Python)"]
        Frontend["🎨 React Frontend<br/>Dashboard UI<br/>(TypeScript)"]
    end
    
    subgraph "Scanners & Tools"
        SBOM["📦 Syft<br/>SBOM Generation"]
        Grype["🔍 Grype<br/>Vuln Scanner"]
        OSV["🌐 OSV Scanner<br/>Google DB"]
        Trivy["🔎 Trivy<br/>Image/FS Scanner"]
    end
    
    subgraph "Remediators"
        OpenRewrite["🔷 OpenRewrite<br/>(JVM)"]
        PipAudit["🐍 pip-audit<br/>(Python)"]
        NpmAudit["📦 npm audit<br/>(JavaScript)"]
        GoVuln["🐹 govulncheck<br/>(Go)"]
        CargoAudit["🦀 cargo-audit<br/>(Rust)"]
    end
    
    subgraph "Repos"
        JVM["☕ JVM App<br/>(Maven/Gradle)"]
        Python["🐍 Python App"]
        Node["📦 Node App"]
        Go["🐹 Go App"]
        Rust["🦀 Rust App"]
    end
    
    User -->|"CLI Command"| CLI
    User -->|"Browser"| Frontend
    
    CLI -->|"Orchestrates"| Core
    Frontend -->|"API Calls"| Backend
    Backend -->|"Orchestrates"| Core
    
    Core -->|"Invokes"| SBOM
    Core -->|"Invokes"| Grype
    Core -->|"Invokes"| OSV
    Core -->|"Invokes"| Trivy
    
    Core -->|"Uses"| OpenRewrite
    Core -->|"Uses"| PipAudit
    Core -->|"Uses"| NpmAudit
    Core -->|"Uses"| GoVuln
    Core -->|"Uses"| CargoAudit
    
    SBOM -->|"Generates"| JVM
    SBOM -->|"Generates"| Python
    SBOM -->|"Generates"| Node
    SBOM -->|"Generates"| Go
    SBOM -->|"Generates"| Rust
    
    Grype -->|"Scans"| JVM
    Grype -->|"Scans"| Python
    Grype -->|"Scans"| Node
    Grype -->|"Scans"| Go
    Grype -->|"Scans"| Rust
    
    OpenRewrite -->|"Remediates"| JVM
    PipAudit -->|"Remediates"| Python
    NpmAudit -->|"Remediates"| Node
    GoVuln -->|"Remediates"| Go
    CargoAudit -->|"Remediates"| Rust
    
    style CLI fill:#fff3e0
    style Core fill:#f3e5f5
    style Backend fill:#e3f2fd
    style Frontend fill:#fce4ec
    style SBOM fill:#e8f5e9
    style Grype fill:#e8f5e9
    style OSV fill:#e8f5e9
    style Trivy fill:#e8f5e9
    style OpenRewrite fill:#fce4ec
    style PipAudit fill:#fce4ec
    style NpmAudit fill:#fce4ec
    style GoVuln fill:#fce4ec
    style CargoAudit fill:#fce4ec
```

---

## 3. Component Diagram — Core Pipeline Architecture

Internal structure of the DepShieldPipeline and module relationships.

```mermaid
graph TB
    subgraph "Entry Point"
        CLI["cli.py<br/>Click Commands"]
    end
    
    subgraph "Configuration & Models"
        Config["config.py<br/>DepShieldConfig"]
        Models["models.py<br/>Vulnerability, ScanResult,<br/>RemediationResult, etc."]
    end
    
    subgraph "Phase 1: Discovery"
        Discovery["discovery.py<br/>RepositoryDiscovery"]
    end
    
    subgraph "Phase 2-3: Scanning"
        Pipeline["pipeline.py<br/>DepShieldPipeline"]
        BaseScanner["scanners/base.py<br/>BaseScanner"]
        Syft["scanners/sbom.py<br/>SyftScanner"]
        Grype["scanners/grype.py<br/>GrypScanner"]
        OSV["scanners/osv.py<br/>OSVScanner"]
        Trivy["scanners/trivy.py<br/>TrivyScanner"]
    end
    
    subgraph "Phase 4: Matrices"
        DepMatrix["matrix/dependency_matrix.py<br/>DependencyMatrix"]
        UpMatrix["matrix/upgrade_matrix.py<br/>UpgradeMatrix"]
    end
    
    subgraph "Phase 5: Remediation"
        BaseRemed["remediation/base.py<br/>BaseRemediator"]
        OpenRewrite["remediation/openrewrite.py<br/>OpenRewriteRemediator"]
        PipUpgrader["remediation/pip_upgrader.py<br/>PipUpgrader"]
        NpmUpgrader["remediation/npm_upgrader.py<br/>NpmUpgrader"]
        GoUpgrader["remediation/go_upgrader.py<br/>GoUpgrader"]
        CargoUpgrader["remediation/cargo_upgrader.py<br/>CargoUpgrader"]
    end
    
    subgraph "Phase 6: Reporting"
        SBOMReport["reporters/sbom_report.py<br/>SBOMReporter"]
        VulnReport["reporters/vuln_report.py<br/>VulnReporter"]
        ArchReport["reporters/architecture.py<br/>ArchitectureReporter"]
        Diagrams["reporters/diagrams.py<br/>DiagramGenerator"]
        CodeGuide["reporters/coding_guidelines.py<br/>GuidelinesReporter"]
        TestCases["reporters/test_cases.py<br/>TestCasesReporter"]
    end
    
    CLI -->|"Uses"| Config
    CLI -->|"Uses"| Models
    CLI -->|"Instantiates"| Pipeline
    
    Discovery -->|"Uses"| Models
    Pipeline -->|"Phase 1"| Discovery
    
    Pipeline -->|"Phase 2-3"| Syft
    Pipeline -->|"Phase 2-3"| Grype
    Pipeline -->|"Phase 2-3"| OSV
    Pipeline -->|"Phase 2-3"| Trivy
    
    Syft -->|"Extends"| BaseScanner
    Grype -->|"Extends"| BaseScanner
    OSV -->|"Extends"| BaseScanner
    Trivy -->|"Extends"| BaseScanner
    
    Pipeline -->|"Phase 4"| DepMatrix
    Pipeline -->|"Phase 4"| UpMatrix
    
    Pipeline -->|"Phase 5"| OpenRewrite
    Pipeline -->|"Phase 5"| PipUpgrader
    Pipeline -->|"Phase 5"| NpmUpgrader
    Pipeline -->|"Phase 5"| GoUpgrader
    Pipeline -->|"Phase 5"| CargoUpgrader
    
    OpenRewrite -->|"Extends"| BaseRemed
    PipUpgrader -->|"Extends"| BaseRemed
    NpmUpgrader -->|"Extends"| BaseRemed
    GoUpgrader -->|"Extends"| BaseRemed
    CargoUpgrader -->|"Extends"| BaseRemed
    
    Pipeline -->|"Phase 6"| SBOMReport
    Pipeline -->|"Phase 6"| VulnReport
    Pipeline -->|"Phase 6"| ArchReport
    Pipeline -->|"Phase 6"| Diagrams
    Pipeline -->|"Phase 6"| CodeGuide
    Pipeline -->|"Phase 6"| TestCases
    
    style Pipeline fill:#f3e5f5,stroke:#7c3aed,stroke-width:3px
    style Discovery fill:#e8f5e9
    style BaseScanner fill:#fff3e0
    style Syft fill:#fff3e0
    style Grype fill:#fff3e0
    style OSV fill:#fff3e0
    style Trivy fill:#fff3e0
    style DepMatrix fill:#e3f2fd
    style UpMatrix fill:#e3f2fd
    style BaseRemed fill:#fce4ec
    style OpenRewrite fill:#fce4ec
    style PipUpgrader fill:#fce4ec
    style NpmUpgrader fill:#fce4ec
    style GoUpgrader fill:#fce4ec
    style CargoUpgrader fill:#fce4ec
    style SBOMReport fill:#ede7f6
    style VulnReport fill:#ede7f6
    style ArchReport fill:#ede7f6
    style Diagrams fill:#ede7f6
    style CodeGuide fill:#ede7f6
    style TestCases fill:#ede7f6
```

---

## 4. Data Flow Diagram — Pipeline Execution

How data flows through the 6 phases of the pipeline.

```mermaid
graph LR
    Start["🚀<br/>Input: Repo Paths<br/>+ Config"]
    
    subgraph "Phase 1: Discovery"
        D1["Walk directories<br/>detect ecosystems"]
        D2["Build RepoManifest<br/>(paths, build/test cmds)"]
        D3["Output: List[RepoManifest]"]
    end
    
    subgraph "Phase 2: SBOM Generation"
        S1["Invoke Syft<br/>per repo (parallel)"]
        S2["Parse CycloneDX<br/>JSON output"]
        S3["Output: SBOMs<br/>+ deps/versions"]
    end
    
    subgraph "Phase 3: Vulnerability Scanning"
        V1["Grype scan<br/>on each SBOM"]
        V2["OSV Scanner<br/>cross-check"]
        V3["Trivy scan<br/>filesystem"]
        V4["Deduplicate<br/>by CVE ID"]
        V5["Output: ScanResult<br/>(vulnerabilities, severity)"]
    end
    
    subgraph "Phase 4: Matrix Building"
        M1["Extract deps<br/>from SBOMs"]
        M2["Cross-repo<br/>dependency table"]
        M3["Group by package<br/>→ safe versions"]
        M4["Output: DependencyMatrix<br/>+ UpgradeMatrix"]
    end
    
    subgraph "Phase 5: Remediation"
        R1{"--apply<br/>flag?"}
        R2["Git stash<br/>current state"]
        R3["Per ecosystem:<br/>run upgrader<br/>(OpenRewrite, pip, etc.)"]
        R4["Run build<br/>+ tests"]
        R5{"Success?"}
        R6["Commit<br/>changes"]
        R7["Git stash pop<br/>rollback"]
        R8["Output: RemediationResult"]
    end
    
    subgraph "Phase 6: Documentation"
        Doc1["Render 11 markdown files<br/>(SBOM, Vuln, Architecture,<br/>Coding Guidelines, etc.)"]
        Doc2["Generate Mermaid<br/>diagrams<br/>(C4, sequence, flowchart)"]
        Doc3["Output: docs/"]
    end
    
    End["✅ Complete<br/>Reports in output_dir"]
    
    Start --> D1 --> D2 --> D3
    D3 --> S1 --> S2 --> S3
    S3 --> V1 --> V2 --> V3 --> V4 --> V5
    V5 --> M1 --> M2 --> M3 --> M4
    M4 --> R1
    R1 -->|"Yes"| R2 --> R3 --> R4 --> R5
    R5 -->|"Yes"| R6 --> R8
    R5 -->|"No"| R7 --> R8
    R1 -->|"No (dry-run)"| R8
    R8 --> Doc1 --> Doc2 --> Doc3
    Doc3 --> End
    
    style Start fill:#e1f5ff
    style D1 fill:#e8f5e9
    style D2 fill:#e8f5e9
    style D3 fill:#e8f5e9
    style S1 fill:#fff3e0
    style S2 fill:#fff3e0
    style S3 fill:#fff3e0
    style V1 fill:#fff3e0
    style V2 fill:#fff3e0
    style V3 fill:#fff3e0
    style V4 fill:#fff3e0
    style V5 fill:#fff3e0
    style M1 fill:#e3f2fd
    style M2 fill:#e3f2fd
    style M3 fill:#e3f2fd
    style M4 fill:#e3f2fd
    style R1 fill:#fce4ec
    style R2 fill:#fce4ec
    style R3 fill:#fce4ec
    style R4 fill:#fce4ec
    style R5 fill:#fce4ec
    style R6 fill:#fce4ec
    style R7 fill:#fce4ec
    style R8 fill:#fce4ec
    style Doc1 fill:#ede7f6
    style Doc2 fill:#ede7f6
    style Doc3 fill:#ede7f6
    style End fill:#c8e6c9
```

---

## 5. Dependency Graph — Ecosystem Integration

Shows how each ecosystem is detected and remediated.

```mermaid
graph TB
    subgraph "JVM Ecosystem"
        POM["pom.xml<br/>build.gradle"]
        Maven["Maven/Gradle<br/>detection"]
        OpenRec["OpenRewrite<br/>recipes"]
        JVMBuild["build command<br/>mvn clean install"]
        JVMOK{"Build<br/>OK?"}
    end
    
    subgraph "Python Ecosystem"
        REQ["requirements.txt<br/>setup.py<br/>pyproject.toml"]
        PyDetect["Python<br/>detection"]
        PipAud["pip-audit<br/>--fix"]
        PyBuild["build command<br/>pytest"]
        PyOK{"Tests<br/>OK?"}
    end
    
    subgraph "JavaScript Ecosystem"
        PKG["package.json<br/>package-lock.json"]
        NodeDetect["Node.js<br/>detection"]
        NpmAud["npm audit<br/>fix --force"]
        NodeBuild["build command<br/>npm test"]
        NodeOK{"Tests<br/>OK?"}
    end
    
    subgraph "Go Ecosystem"
        GOMOD["go.mod<br/>go.sum"]
        GoDetect["Go<br/>detection"]
        GoVul["go get -u<br/>govulncheck"]
        GoBuild["build command<br/>go test"]
        GoOK{"Tests<br/>OK?"}
    end
    
    subgraph "Rust Ecosystem"
        TOML["Cargo.toml<br/>Cargo.lock"]
        RustDetect["Rust<br/>detection"]
        CargoAud["cargo update<br/>cargo-audit fix"]
        RustBuild["build command<br/>cargo test"]
        RustOK{"Tests<br/>OK?"}
    end
    
    subgraph "Shared Flow"
        Discover["RepositoryDiscovery"]
        Pipeline["DepShieldPipeline"]
        Rollback["Git Stash<br/>Rollback on Fail"]
    end
    
    Discover -->|"Detects"| POM
    Discover -->|"Detects"| REQ
    Discover -->|"Detects"| PKG
    Discover -->|"Detects"| GOMOD
    Discover -->|"Detects"| TOML
    
    POM --> Maven --> OpenRec
    REQ --> PyDetect --> PipAud
    PKG --> NodeDetect --> NpmAud
    GOMOD --> GoDetect --> GoVul
    TOML --> RustDetect --> CargoAud
    
    OpenRec --> JVMBuild --> JVMOK
    PipAud --> PyBuild --> PyOK
    NpmAud --> NodeBuild --> NodeOK
    GoVul --> GoBuild --> GoOK
    CargoAud --> RustBuild --> RustOK
    
    JVMOK --> Rollback
    PyOK --> Rollback
    NodeOK --> Rollback
    GoOK --> Rollback
    RustOK --> Rollback
    
    Pipeline -.->|"Orchestrates"| Discover
    Pipeline -.->|"Uses"| OpenRec
    Pipeline -.->|"Uses"| PipAud
    Pipeline -.->|"Uses"| NpmAud
    Pipeline -.->|"Uses"| GoVul
    Pipeline -.->|"Uses"| CargoAud
    
    style POM fill:#e0e4ff
    style Maven fill:#e0e4ff
    style OpenRec fill:#c8d9f1
    style REQ fill:#ffeaa7
    style PyDetect fill:#ffeaa7
    style PipAud fill:#ffd54f
    style PKG fill:#e0f2f1
    style NodeDetect fill:#e0f2f1
    style NpmAud fill:#80deea
    style GOMOD fill:#fff3e0
    style GoDetect fill:#fff3e0
    style GoVul fill:#ffb74d
    style TOML fill:#f3e5f5
    style RustDetect fill:#f3e5f5
    style CargoAud fill:#ce93d8
```

---

## 6. Scanner Integration — Multi-Source Vulnerability Detection

Parallel invocation and result aggregation of scanners.

```mermaid
graph TB
    Repo["Repository<br/>with dependencies"]
    
    subgraph "Step 1: SBOM Generation"
        Syft["🔷 Syft"]
    end
    
    subgraph "Step 2: Parallel Scanning"
        Grype["🔍 Grype<br/>(Database: Grype DB)"]
        OSV["🌐 OSV Scanner<br/>(Database: Google OSV)"]
        Trivy["🔎 Trivy<br/>(Database: GitHub Advisories)"]
    end
    
    subgraph "Step 3: Aggregation"
        Parse1["Parse JSON<br/>results"]
        Parse2["Parse JSON<br/>results"]
        Parse3["Parse JSON<br/>results"]
        Dedup["Deduplicate<br/>by CVE ID"]
        Score["Score by<br/>Severity:<br/>CRITICAL<br/>HIGH<br/>MEDIUM<br/>LOW"]
    end
    
    subgraph "Output"
        Result["ScanResult<br/>├─ Vulnerabilities list<br/>├─ SBOM<br/>└─ Severity breakdown"]
    end
    
    Repo -->|"Generate"| Syft
    Syft -->|"CycloneDX.json"| Grype
    Syft -->|"CycloneDX.json"| OSV
    Syft -->|"CycloneDX.json"| Trivy
    
    Grype -->|"JSON"| Parse1
    OSV -->|"JSON"| Parse2
    Trivy -->|"JSON"| Parse3
    
    Parse1 --> Dedup
    Parse2 --> Dedup
    Parse3 --> Dedup
    
    Dedup --> Score
    Score --> Result
    
    style Syft fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style Grype fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style OSV fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Trivy fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    style Dedup fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style Score fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style Result fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
```

---

## 7. Remediation Process Flow

Step-by-step remediation with safety gates and rollback.

```mermaid
graph TD
    Start["🚀 Remediation Phase"]
    Check{"--apply<br/>flag?"}
    SkipRemed["Skip remediation<br/>(dry-run mode)"]
    
    Stash["📦 Git Stash<br/>Save current state"]
    
    PerRepo["For each repository:"]
    PerEco["For each detected ecosystem:"]
    
    Detect{"Which<br/>Ecosystem?"}
    
    OpenRec["🔷 OpenRewrite<br/>Maven/Gradle"]
    PipFix["🐍 pip-audit --fix<br/>Python"]
    NpmFix["📦 npm audit fix<br/>Node.js"]
    GoGet["🐹 go get -u<br/>Go"]
    CargUpd["🦀 cargo update<br/>Rust"]
    
    BuildTest["🔨 Run build<br/>+ test commands"]
    
    Success{"Build &<br/>Tests<br/>OK?"}
    
    Commit["✅ Keep changes<br/>Git add + commit"]
    Rollback["⚠️  Rollback changes<br/>git stash pop"]
    
    LogResult["📝 Log result:<br/>✓ Successful<br/>✗ Failed<br/>✗ Skipped"]
    
    AllDone["All repos<br/>processed"]
    
    Done["✅ Remediation Complete<br/>Report: RemediationResult"]
    
    Start --> Check
    Check -->|"No"| SkipRemed --> AllDone
    Check -->|"Yes"| Stash
    
    Stash --> PerRepo --> PerEco
    
    PerEco --> Detect
    Detect -->|"JVM"| OpenRec
    Detect -->|"Python"| PipFix
    Detect -->|"JavaScript"| NpmFix
    Detect -->|"Go"| GoGet
    Detect -->|"Rust"| CargUpd
    
    OpenRec --> BuildTest
    PipFix --> BuildTest
    NpmFix --> BuildTest
    GoGet --> BuildTest
    CargUpd --> BuildTest
    
    BuildTest --> Success
    Success -->|"Yes"| Commit --> LogResult
    Success -->|"No"| Rollback --> LogResult
    
    LogResult --> AllDone
    AllDone --> Done
    
    style Start fill:#e1f5ff
    style Check fill:#fff3e0
    style Stash fill:#ffccbc
    style OpenRec fill:#c8d9f1
    style PipFix fill:#ffd54f
    style NpmFix fill:#80deea
    style GoGet fill:#ffb74d
    style CargUpd fill:#ce93d8
    style BuildTest fill:#f8bbd0
    style Success fill:#fff3e0
    style Commit fill:#c8e6c9
    style Rollback fill:#ffcdd2
    style Done fill:#a5d6a7,stroke:#388e3c,stroke-width:3px
```

---

## 8. Web Dashboard Architecture

Frontend-Backend communication and state management.

```mermaid
graph TB
    subgraph "Browser"
        RunForm["RunForm<br/>repo paths,<br/>flags"]
        RunList["RunList<br/>all runs"]
        RunDetail["RunDetail<br/>summary,<br/>status"]
        VulnTable["VulnTable<br/>filterable<br/>vulnerabilities"]
        MatrixView["MatrixView<br/>dep + upgrade<br/>matrices"]
        ReportViewer["ReportViewer<br/>markdown<br/>docs"]
        ScanLog["ScanLog<br/>live SSE<br/>log stream"]
    end
    
    subgraph "Frontend API"
        API["api.ts<br/>fetch wrappers"]
    end
    
    subgraph "FastAPI Backend"
        MainApp["main.py<br/>app factory"]
        Store["store.py<br/>RunState dict"]
        RunsRoute["routes/runs.py<br/>POST/GET /runs"]
        LogsRoute["routes/logs.py<br/>SSE stream"]
        VulnRoute["routes/vulns.py<br/>filter & search"]
        MatrixRoute["routes/matrix.py<br/>dep + upgrade"]
        ReportsRoute["routes/reports.py<br/>markdown files"]
    end
    
    subgraph "Core Pipeline"
        PiplineExec["DepShieldPipeline<br/>6 phases"]
    end
    
    subgraph "Async Job Queue"
        BGTask["Background Task<br/>run_pipeline(run_id)"]
        LogHandler["Custom LogHandler<br/>→ RunState.logs"]
    end
    
    RunForm -->|"POST /api/runs"| API
    API --> RunsRoute
    RunsRoute -->|"create"| Store
    RunsRoute -->|"launch"| BGTask
    BGTask -->|"execute"| PiplineExec
    PiplineExec -->|"append logs"| LogHandler
    LogHandler -->|"update"| Store
    
    RunList -->|"GET /api/runs"| API
    API --> RunsRoute
    RunsRoute -->|"read"| Store
    
    RunDetail -->|"GET /api/runs/:id"| API
    API --> RunsRoute
    RunsRoute -->|"read"| Store
    
    ScanLog -->|"GET /api/runs/:id/logs (SSE)"| API
    API --> LogsRoute
    LogsRoute -->|"stream"| Store
    
    VulnTable -->|"GET /api/runs/:id/vulnerabilities"| API
    API --> VulnRoute
    VulnRoute -->|"filter"| Store
    
    MatrixView -->|"GET /api/runs/:id/matrix/*"| API
    API --> MatrixRoute
    MatrixRoute -->|"read"| Store
    
    ReportViewer -->|"GET /api/runs/:id/repos/:name/reports/:file"| API
    API --> ReportsRoute
    ReportsRoute -->|"read file"| PiplineExec
    
    style RunForm fill:#fce4ec
    style RunList fill:#fce4ec
    style RunDetail fill:#fce4ec
    style VulnTable fill:#fce4ec
    style MatrixView fill:#fce4ec
    style ReportViewer fill:#fce4ec
    style ScanLog fill:#fce4ec
    style API fill:#f3e5f5
    style MainApp fill:#e3f2fd
    style Store fill:#e3f2fd
    style RunsRoute fill:#e3f2fd
    style LogsRoute fill:#e3f2fd
    style VulnRoute fill:#e3f2fd
    style MatrixRoute fill:#e3f2fd
    style ReportsRoute fill:#e3f2fd
    style BGTask fill:#fff3e0
    style LogHandler fill:#fff3e0
    style PiplineExec fill:#f3e5f5,stroke:#7c3aed,stroke-width:2px
```

---

## 9. Deployment Architecture

CLI, Docker, and CI/CD deployment models.

```mermaid
graph TB
    subgraph "Development"
        Laptop["💻 Developer Laptop"]
        VirtualEnv["Virtual Environment<br/>pip install -e ."]
    end
    
    subgraph "CLI Deployment"
        CLI["depshield command<br/>(entry point)"]
    end
    
    subgraph "Docker Deployment"
        Dockerfile["Dockerfile<br/>Python 3.12<br/>+ all tools"]
        Image["depshield:latest<br/>Docker Image"]
        Container["Container<br/>mounted repos"]
    end
    
    subgraph "CI/CD Integration"
        GHActions["GitHub Actions<br/>.github/workflows/"]
        GitLabCI["GitLab CI<br/>.gitlab-ci.yml"]
        CIPipeline["Pipeline stages:<br/>scan → remediate"]
    end
    
    subgraph "Output"
        LocalOutput["Local filesystem<br/>./depshield-output/"]
        ArtifactUpload["Artifacts upload<br/>(GitHub/GitLab)"]
        PRComments["PR Comments<br/>with summary"]
    end
    
    Laptop -->|"pip install"| VirtualEnv
    VirtualEnv -->|"runs"| CLI
    CLI -->|"scans/remediates"| LocalOutput
    
    Dockerfile -->|"builds"| Image
    Image -->|"runs"| Container
    Container -->|"mounts"| LocalOutput
    
    GHActions -->|"uses"| Image
    GitLabCI -->|"uses"| Image
    GHActions -->|"runs"| CIPipeline
    GitLabCI -->|"runs"| CIPipeline
    
    CIPipeline -->|"outputs"| ArtifactUpload
    ArtifactUpload -->|"comments on"| PRComments
    
    style Laptop fill:#e1f5ff
    style VirtualEnv fill:#c8e6c9
    style CLI fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Dockerfile fill:#ede7f6
    style Image fill:#ede7f6
    style Container fill:#ede7f6
    style GHActions fill:#f3e5f5
    style GitLabCI fill:#f3e5f5
    style CIPipeline fill:#e3f2fd
    style LocalOutput fill:#c8e6c9
    style ArtifactUpload fill:#c8e6c9
    style PRComments fill:#c8e6c9
```

---

## 10. Data Model Relationships

Entity relationship diagram showing core dataclasses.

```mermaid
erDiagram
    RepoManifest ||--o{ Ecosystem : "has"
    RepoManifest ||--o{ Vulnerability : "detects"
    RepoManifest ||--o{ Dependency : "contains"
    
    ScanResult ||--o{ Vulnerability : "reports"
    ScanResult ||--o{ Dependency : "tracks"
    
    Vulnerability ||--|| Severity : "rated"
    Vulnerability ||--|| Ecosystem : "affects"
    
    DependencyMatrix ||--o{ Dependency : "indexes"
    UpgradeMatrix ||--o{ Vulnerability : "maps to fix"
    
    RemediationResult ||--o{ Vulnerability : "fixed"
    RemediationResult ||--|| RepoManifest : "applied to"
    
    SystemSBOM ||--o{ RepoManifest : "aggregates"
    
    RepoManifest {
        string path
        string name
        list ecosystems
        dict build_command
        dict test_command
        dict lint_command
    }
    
    Vulnerability {
        string cve_id
        string package_name
        string current_version
        string safe_version
        string description
        severity severity
        float cvss_score
        string ecosystem
    }
    
    Dependency {
        string name
        string version
        string ecosystem
        list repos_using
    }
    
    Ecosystem {
        string name
        string manifest_file
        string scanner_tool
        string remediation_tool
    }
    
    Severity {
        string CRITICAL
        string HIGH
        string MEDIUM
        string LOW
    }
    
    ScanResult {
        list vulnerabilities
        list dependencies
        string sbom_path
        datetime scanned_at
    }
    
    DependencyMatrix {
        dict matrix
        list conflicts
    }
    
    UpgradeMatrix {
        dict recommendations
        list safe_versions
    }
    
    RemediationResult {
        string status
        list applied_recipes
        string build_output
        string test_output
        boolean success
    }
    
    SystemSBOM {
        list sboms
        list all_vulnerabilities
        list ecosystem_summary
    }
```

---

## 11. Request-Response Flow — Dashboard Example

Complete flow of a user triggering a scan through the dashboard.

```mermaid
sequenceDiagram
    actor User
    participant UI as React<br/>Frontend
    participant Browser as Browser Cache
    participant Backend as FastAPI<br/>Backend
    participant Store as RunState<br/>Store
    participant Pipeline as DepShield<br/>Pipeline
    participant Logger as Log<br/>Handler
    
    User->>UI: Fill form: repos, flags
    User->>UI: Click "Start Scan"
    
    UI->>Backend: POST /api/runs { repos, dry_run, apply }
    activate Backend
    Backend->>Store: Create RunState(id, status=pending)
    Backend->>Backend: create_task(run_pipeline)
    Backend-->>UI: { run_id }
    deactivate Backend
    
    UI->>Browser: Store run_id
    UI->>UI: Navigate to /runs/:id
    
    Backend->>Pipeline: Start background task
    activate Pipeline
    Pipeline->>Logger: Attach custom handler
    
    loop Phase 1-6
        Pipeline->>Logger: log(message)
        Logger->>Store: Append to RunState.logs
    end
    
    UI->>Backend: GET /api/runs/:id/logs (SSE)
    activate Backend
    Backend->>Store: Stream RunState.logs
    Backend-->>UI: log line 1
    Backend-->>UI: log line 2
    Backend-->>UI: log line 3
    deactivate Backend
    
    UI->>UI: Display live logs
    
    Pipeline->>Store: Update status=done
    Pipeline->>Store: Set scan_results
    Pipeline->>Store: Set matrices
    deactivate Pipeline
    
    UI->>Backend: GET /api/runs/:id
    Backend->>Store: Read RunState
    Backend-->>UI: { status, vulnerabilities, matrices }
    
    UI->>UI: Display summary
    UI->>UI: Render vuln table
    UI->>UI: Render matrices
    
    User->>UI: Click on repo name
    UI->>Backend: GET /api/runs/:id/repos/repo-name/reports/VULNERABILITY_REPORT.md
    Backend-->>UI: Markdown content
    
    UI->>UI: render-markdown + Mermaid
    User->>User: Read detailed report
```

---

## Summary

These diagrams provide comprehensive views of DepShield at multiple levels:

- **C4 Context**: System boundary and external actors
- **C4 Container**: Major components and communication
- **Components**: Internal module structure
- **Data Flow**: How data moves through the pipeline
- **Dependencies**: Ecosystem-specific integration points
- **Scanners**: Multi-source vulnerability detection
- **Remediation**: Safety gates and rollback mechanisms
- **Dashboard**: Frontend-Backend architecture
- **Deployment**: CLI, Docker, and CI/CD models
- **Data Models**: Entity relationships
- **Sequences**: Request-response flows

All diagrams are production-ready and follow professional draw.io standards with consistent color coding, clear relationships, and detailed annotations.
