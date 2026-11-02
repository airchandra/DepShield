# DepShield — Quick Start Guide

Get up and running in 5 minutes.

## Prerequisites

- Python 3.11+
- Node.js 18+ (for dashboard)
- Git

## Option 1: CLI Only (2 minutes)

```bash
cd /Users/sirivennela/source/depshield

# Install
pip install -e .

# Verify
depshield --help

# Scan a repository (dry-run)
depshield --repos /path/to/your/repo --output ./reports --dry-run --verbose

# View results
cat reports/UPGRADE_MATRIX.md
ls -la /path/to/your/repo/docs/
```

**What you get**: 11 markdown files with vulnerability analysis, matrices, and architecture diagrams.

---

## Option 2: Dashboard (5 minutes)

### Backend

```bash
cd /Users/sirivennela/source/depshield/ui/backend

# Install dependencies
pip install -r requirements.txt

# Run server (starts on http://localhost:8000)
uvicorn main:app --reload
```

### Frontend (new terminal)

```bash
cd /Users/sirivennela/source/depshield/ui/frontend

# Install dependencies
npm install

# Run dev server (starts on http://localhost:5173)
npm run dev
```

### Visit Dashboard

Open your browser to **http://localhost:5173**

Fill in the form:
- Repos: `/path/to/your/repo`
- Mode: `Dry Run`
- Ecosystems: Select all or your ecosystem
- Click "Start Scan"

Watch the live logs and explore results!

---

## Option 3: Docker (3 minutes)

### Build

```bash
cd /Users/sirivennela/source/depshield

docker build -t depshield:latest -f docker/Dockerfile .
```

### Run CLI

```bash
docker run -v /path/to/repos:/repos depshield:latest \
  depshield --repos /repos --output /output --dry-run
```

### Run Dashboard

```bash
REPOS_PATH=/path/to/repos OUTPUT_PATH=./output \
docker-compose -f docker/docker-compose.yml up
```

Visit **http://localhost:8000** (dashboard served from FastAPI)

---

## File Overview

After a scan, you'll find:

**In your repository:**
```
/path/to/your/repo/docs/
├── SBOM.md                      # Software bill of materials
├── VULNERABILITY_REPORT.md      # Detailed CVE list
├── ARCHITECTURE.md              # C4 component diagram
├── CODING_GUIDELINES.md         # Detected conventions
├── SEQUENCE_DIAGRAMS.md         # Flowchart diagrams
├── TEST_CASES.md                # Test templates
└── UPGRADE_PLAN.md              # Specific upgrades needed
```

**System-wide:**
```
./depshield-output/
├── SYSTEM_ARCHITECTURE.md       # Full system C4 diagram
├── DEPENDENCY_MATRIX.md         # Cross-repo dependencies
├── UPGRADE_MATRIX.md            # Global upgrade plan
└── PIPELINE_SEQUENCE.md         # Pipeline execution flow
```

All Markdown files include **Mermaid diagrams** for visual representation.

---

## Common Commands

### CLI

```bash
# Dry-run scan (no mutations)
depshield --repos ./api ./frontend --dry-run

# Apply remediation (after review)
depshield --repos ./api ./frontend --no-dry-run --apply --verbose

# Specific ecosystems only
depshield --repos ./project --ecosystems jvm python

# Custom output directory
depshield --repos ./project --output ./my-reports
```

### Dashboard

```bash
# Start both backend and frontend together
cd ui && make dev

# Or individually:
cd ui/backend && make dev-backend
cd ui/frontend && make dev-frontend

# Build for production
cd ui/frontend && npm run build
```

### Docker

```bash
# Build image
docker build -t depshield:latest .

# Run with Docker Compose
docker-compose up

# Scale to multiple repos
docker run -v /repos1:/repos depshield:latest ...
docker run -v /repos2:/repos depshield:latest ...
```

---

## Deployment Checklist

- [ ] Install dependencies: `pip install -e .`
- [ ] Run a test scan: `depshield --repos . --dry-run`
- [ ] Review reports in `./docs/`
- [ ] (Optional) Start dashboard: `cd ui && make dev`
- [ ] (Optional) Build Docker: `docker build -t depshield .`
- [ ] (CI/CD) Copy templates: `cp ci-templates/* .github/workflows/`

---

## Troubleshooting

**"depshield: command not found"**
```bash
pip install -e /Users/sirivennela/source/depshield
```

**"ModuleNotFoundError: No module named 'harness'"**
```bash
cd /Users/sirivennela/source/depshield
pip install -e .
```

**"Cannot find Syft/Grype/Trivy"**
→ Use Docker instead, or install tools separately
```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
```

**Frontend won't start**
```bash
cd ui/frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## Next Steps

1. **Read** the main README: `/Users/sirivennela/source/depshield/README.md`
2. **Try it** with your own repo
3. **Deploy** via Docker or CI/CD
4. **Share** results with your team

---

## Support

- **Issues**: Check TROUBLESHOOTING section above
- **Docs**: See `/docs/` directory
- **Code**: Review `/depshield/` for implementation details

🚀 **You're all set! Start scanning!**
