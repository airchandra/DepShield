# DepShield Architecture Diagrams - Draw.io Specifications

This document provides detailed specifications for creating professional architecture diagrams in Draw.io.

---

## 1. C4 Context Diagram

**Dimensions:** 1200 x 800px

### Components:

**User (Top Left)**
- Shape: Actor/Stick figure
- Label: "👤 User\n(Security/DevOps Engineer)"
- Color: #E3F2FD (light blue background)
- Position: 100, 100

**DepShield System (Center Large Box)**
- Shape: Rectangle with rounded corners
- Label: "DepShield System"
- Dimensions: 600 x 400
- Color: White with #2196F3 border (2px)
- Position: 250, 250

**Git Repositories (Right)**
- Shape: Folder/Container
- Label: "Git Repositories\n(Multi-ecosystem)"
- Color: #E8F5E9 (light green)
- Position: 950, 300

**External Systems (Top Right)**
- Shape: Box
- Label: "GitHub\n(Source Control)"
- Color: #FCE4EC (light pink)
- Position: 950, 150

**Connections (Arrows):**
- User → DepShield: Label "Commands"
- User → GitHub: Label "Browse"
- DepShield → Repositories: Label "Scans & Remediates"
- Repositories → GitHub: Label "Push"

---

## 2. Container Diagram

**Dimensions:** 1400 x 1000px

### Main Container Groups:

**DepShield System Container (Left, centered)**
- Dimensions: 800 x 600
- Color: White with blue border

**Inside DepShield Container:**

1. **CLI (Command Line Interface)**
   - Shape: Box with gradient (light yellow to white)
   - Label: "🖥️ Click CLI\nPython"
   - Position: 50, 50 (relative to container)
   - Dimensions: 200 x 120

2. **Core Pipeline**
   - Shape: Box with gradient (light purple)
   - Label: "🔧 Core Pipeline\nPython"
   - Position: 300, 50
   - Dimensions: 200 x 120

3. **FastAPI Backend**
   - Shape: Box with gradient (light blue)
   - Label: "⚙️ FastAPI Backend\nREST + SSE"
   - Position: 550, 50
   - Dimensions: 200 x 120

4. **React Frontend**
   - Shape: Box with gradient (light pink)
   - Label: "🎨 React Frontend\nTypeScript"
   - Position: 50, 200
   - Dimensions: 200 x 120

**External Systems (Right side)**

1. **Scanners Group** (Positions arranged vertically)
   - 📦 Syft (Light green)
   - 🔍 Grype (Light green)
   - 🌐 OSV Scanner (Light blue)
   - 🔎 Trivy (Light pink)

2. **Remediators Group** (Positions arranged vertically)
   - 🔷 OpenRewrite (Light pink)
   - 🐍 pip-audit (Light yellow)
   - 📦 npm audit (Light cyan)
   - 🐹 govulncheck (Light orange)
   - 🦀 cargo-audit (Light purple)

3. **Repositories** (Arranged vertically)
   - ☕ JVM App (Maven/Gradle)
   - 🐍 Python App
   - 📦 Node App
   - 🐹 Go App
   - 🦀 Rust App

**Connections:**
- CLI → Core Pipeline (Orchestrates)
- Frontend → Backend (API Calls)
- Backend → Core Pipeline (Orchestrates)
- Core Pipeline → All Scanners (Invokes)
- Core Pipeline → All Remediators (Uses)
- Scanners → Repositories (Scans)
- Remediators → Repositories (Remediates)

---

## 3. Component/Module Diagram

**Dimensions:** 1600 x 1200px

**Layout:** Tree structure from top to bottom

**Root: CLI (Top)**
- Shape: Rectangle
- Label: "cli.py\nClick Commands"
- Color: #FFF3E0

**Level 2 (Configuration & Models)**
- Left: config.py (Color: #F3E5F5)
- Right: models.py (Color: #F3E5F5)

**Level 3 (Core Pipeline)**
- Center: pipeline.py (Large box, Color: #F3E5F5)
- Connected to: discovery.py

**Level 4 (Subsystems)**

1. **Scanners Subsystem** (Left branch)
   - base.py
   - sbom.py (Syft)
   - grype.py
   - osv.py
   - trivy.py
   - Color: #FFF3E0

2. **Remediation Subsystem** (Center branch)
   - base.py
   - openrewrite.py
   - pip_upgrader.py
   - npm_upgrader.py
   - go_upgrader.py
   - cargo_upgrader.py
   - Color: #FCE4EC

3. **Matrix Subsystem** (Right branch)
   - dependency_matrix.py
   - upgrade_matrix.py
   - Color: #E3F2FD

4. **Reporters Subsystem** (Bottom)
   - architecture.py
   - diagrams.py
   - sbom_report.py
   - vuln_report.py
   - coding_guidelines.py
   - test_cases.py
   - Color: #EDE7F6

**Connectors:**
- All subsystems connect back to pipeline.py with labeled arrows
- Color: #2196F3 for active connections
- Dashed lines for optional/conditional connections

---

## 4. Data Flow Diagram (6-Phase Pipeline)

**Dimensions:** 1800 x 400px
**Layout:** Horizontal flow (left to right)

### Six Phases (Each in a box):

1. **Phase 1: Discovery**
   - Color: #E8F5E9
   - Content: "Walk directories\nDetect ecosystems\nBuild manifests"
   - Output: "List[RepoManifest]"

2. **Phase 2: SBOM Generation**
   - Color: #FFF3E0
   - Content: "Invoke Syft\nParse JSON\nExtract deps"
   - Output: "SBOMs"

3. **Phase 3: Vulnerability Scanning**
   - Color: #FFF3E0
   - Content: "Grype scan\nOSV Scanner\nTrivy scan\nDeduplicate"
   - Output: "ScanResult"

4. **Phase 4: Matrix Building**
   - Color: #E3F2FD
   - Content: "Extract deps\nCross-repo table\nSafe versions\nGroup packages"
   - Output: "Matrices"

5. **Phase 5: Remediation**
   - Color: #FCE4EC
   - Content: "Git stash\nRun upgraders\nBuild + test\nRollback/Commit"
   - Output: "RemediationResult"

6. **Phase 6: Documentation**
   - Color: #EDE7F6
   - Content: "Render Markdown\nGenerate diagrams\nFormat reports"
   - Output: "docs/"

### Flow Arrows:
- Connect phases left to right
- Label each arrow with data passing through
- Use gradient colors to show data transformation

---

## 5. Web Dashboard Architecture

**Dimensions:** 1400 x 800px

### Left Side: Browser (Container)
- Components arranged as boxes:
  - RunForm (Color: #FCE4EC)
  - RunList (Color: #FCE4EC)
  - RunDetail (Color: #FCE4EC)
  - VulnTable (Color: #FCE4EC)
  - MatrixView (Color: #FCE4EC)
  - ReportViewer (Color: #FCE4EC)

### Middle: Frontend API
- Box: "api.ts\nFetch wrappers"
- Color: #F3E5F5

### Right Side: Backend Components
- **main.py** (Color: #E3F2FD)
  - With sub-boxes for middleware, routes
- **Routes/** (Color: #E3F2FD)
  - runs.py
  - logs.py
  - vulns.py
  - matrix.py
  - reports.py
- **store.py** (Color: #E3F2FD)
- **models.py** (Color: #E3F2FD)

### Connection Flows:
- Browser components → api.ts → Backend routes
- Backend routes ↔ store.py (bidirectional)
- All with labeled arrows showing data flow

---

## 6. Deployment Architecture

**Dimensions:** 1200 x 900px

### Three Deployment Models:

**1. CLI Deployment (Left)**
- Developer Laptop → venv → depshield command → Local repos

**2. Docker Deployment (Center)**
- Dockerfile → Docker Image → Container → mounted repos

**3. CI/CD Deployment (Right)**
- GitHub Actions / GitLab CI → Pipeline stages → Artifact upload → PR comments

### Connections show data flow between models

---

## 7. Ecosystem Integration Flow

**Dimensions:** 1600 x 1000px

### Five Parallel Tracks (one for each ecosystem):

**Each Track includes:**
1. Manifest File (e.g., pom.xml, package.json)
2. Detection (e.g., Maven Detection, Node Detection)
3. Upgrader Tool (e.g., OpenRewrite, npm audit)
4. Build Command (e.g., mvn clean install)
5. Test Verification
6. Success/Rollback Decision
7. Logging/Reporting

### Colors by Ecosystem:
- JVM: #E0E4FF (light blue-purple)
- Python: #FFEAA7 (light yellow)
- Node: #E0F2F1 (light teal)
- Go: #FFF3E0 (light orange)
- Rust: #F3E5F5 (light purple)

---

## Color Scheme (Consistent Across All Diagrams)

```
Primary Colors:
- Blue (#2196F3, #1976D2) - Actions, primary flow
- Green (#4CAF50, #E8F5E9) - Success, discovery
- Orange (#FF9800, #FFF3E0) - Scanning, tools
- Purple (#7C3AED, #EDE7F6) - Reporting, data structures
- Pink (#EC407A, #FCE4EC) - Backend, APIs
- Cyan (#00BCD4, #E0F2F1) - Configuration, frontend

Accent Colors:
- Red (#f44336) - Critical/Errors
- Yellow (#FFD54F) - Warnings/Medium
- Light Gray (#F5F5F5) - Backgrounds
- Dark Gray (#333333) - Text
```

---

## Typography Standards

- **Headers:** Bold, 16-18px, Dark Gray
- **Labels:** Regular, 13-14px, Dark Gray
- **Descriptions:** Regular, 11-12px, Medium Gray
- **Monospace for code:** 11px, Monaco/Courier

---

## Creation Steps in Draw.io

1. **Create new diagram** - Start with blank canvas
2. **Set up grid** - 20px grid for alignment
3. **Add component boxes** - Use rectangles with rounded corners
4. **Color components** - Apply colors from scheme
5. **Add connectors** - Use arrows between components
6. **Add labels** - Double-click boxes to add text
7. **Arrange layout** - Use alignment tools (Arrange menu)
8. **Add legend** - Create color/shape legend
9. **Export** - Save as draw.io file + PNG/SVG for documents

---

## Recommended Draw.io Features to Use

- **Containers** - For grouping related components
- **Rounded rectangles** - For software components
- **Cylinders** - For databases/storage
- **Actors** - For users
- **Arrows** - For data flow (use different styles for different flow types)
- **Shapes** - For special components (cloud, folder, etc.)
- **Connectors** - Auto-layout for clean diagrams

---

## Import/Export Guidelines

- **Format:** .drawio XML + PNG/SVG for documentation
- **Resolution:** 300 DPI for print, 72 DPI for web
- **Size:** Optimize for web (max 1600px width)
- **Accessibility:** Add alt text for each diagram

---

This specification can be used to create professional, draw.io-quality diagrams that accurately represent the DepShield architecture at multiple levels of detail.
