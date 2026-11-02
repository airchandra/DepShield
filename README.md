# DepShield — Zero-Critical-Vulnerabilities Pipeline

Automated vulnerability scanning, remediation, and comprehensive documentation for distributed systems. DepShield treats your multi-repo ecosystem as an interconnected whole, not isolated components.

---

## 📖 Documentation Hub

**New to DepShield?**
- 🚀 [QUICKSTART.md](./QUICKSTART.md) — Get started in 5 minutes
- 📚 [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md) — Detailed setup guide

**Want to understand the project?**
- 💡 [intent.md](./intent.md) — Vision and goals
- 🎯 [soul.md](./soul.md) — Core values and philosophy
- 📊 [plan.md](./plan.md) — Roadmap and future direction

**Need technical details?**
- 🔧 [spec.md](./spec.md) — Complete technical specifications
- 🏗️ [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — System design
- 👨‍💻 [claude.md](./claude.md) — Development guide for contributors

**Everything else?**
- 📑 [SPECS.md](./SPECS.md) — Complete documentation index
- ✅ [COMPLETE.md](./COMPLETE.md) — Project completion summary

---

## Features

- **Multi-Ecosystem Support**: JVM (Maven/Gradle), Python (pip), JavaScript (npm), Go (go mod), Rust (Cargo)
- **Comprehensive Scanning**: Syft (SBOM) + Grype + OSV Scanner + Trivy for vulnerability detection
- **Intelligent Remediation**: OpenRewrite (JVM), pip-audit, npm audit, govulncheck, cargo-audit
- **System-Wide Analysis**: 
  - Dependency matrix showing cross-repo usage
  - Upgrade matrix with safe version recommendations
  - Shared dependency conflict detection
- **Rich Documentation**: Auto-generated Markdown files with:
  - CycloneDX SBOM format
  - Detailed vulnerability reports
  - Architecture diagrams (C4 model with Mermaid)
  - Coding guidelines and conventions
  - Test case templates
  - Upgrade plans with remediation sequences
- **Three Deployment Models**:
  - CLI: `pip install depshield && depshield --repos ./a ./b`
  - Docker: `docker run -v ./repos:/repos depshield:latest`
  - CI/CD: GitHub Actions and GitLab CI templates included

## 📚 Complete Documentation

### Project Specifications
Comprehensive documentation of the entire project:

- **[intent.md](./intent.md)** — Vision, goals, and problem we're solving
  - Why DepShield exists
  - Core objectives and principles
  - Target audience and success criteria
  
- **[spec.md](./spec.md)** — Technical and functional specifications
  - API endpoints, data models, CLI commands
  - All 6 pipeline phases in detail
  - Performance targets and compatibility matrix
  
- **[plan.md](./plan.md)** — Roadmap, phases, and implementation strategy
  - 5 phases from MVP to market leader
  - Q1-Q2 2025 milestones
  - Financial projections and resource planning
  
- **[soul.md](./soul.md)** — Design philosophy and core values
  - 6 core principles (Safety, Transparency, Simplicity, etc.)
  - Engineering philosophy and decision framework
  - The "right tool" philosophy
  
- **[claude.md](./claude.md)** — Development guide for contributors
  - Code style and conventions
  - How to add new ecosystems
  - Common tasks and anti-patterns to avoid
  
- **[SPECS.md](./SPECS.md)** — Index and navigation guide
  - Quick navigation by role and question
  - Relationship between documents
  - What these specifications provide

### Other Documentation

- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** — System design and architecture
- **[docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md)** — Step-by-step tutorial
- **[QUICKSTART.md](./QUICKSTART.md)** — 5-minute quick start
- **[COMPLETE.md](./COMPLETE.md)** — Project completion summary
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** — Feature breakdown

### Dashboard Documentation

- **[ui/README.md](./ui/README.md)** — Web dashboard setup and API reference

---

## Quick Start

### Installation

```bash
# From source
git clone https://github.com/yourusername/depshield.git
cd depshield
pip install -e .

# Verify
depshield --help
```

### Basic Usage

```bash
# Dry-run scan (generates reports, no mutations)
depshield --repos ./my-jvm-app ./my-node-app --output ./reports --dry-run

# Apply remediations (after review)
depshield --repos ./my-jvm-app ./my-node-app --output ./reports --no-dry-run --apply
```

### Docker

```bash
# Build image
docker build -t depshield:latest -f docker/Dockerfile .

# Run with docker-compose
REPOS_PATH=./repos OUTPUT_PATH=./output docker-compose -f docker/docker-compose.yml up

# Or direct docker
docker run -v ./repos:/repos -v ./output:/output depshield:latest \
  depshield --repos /repos --output /output --dry-run
```

## Pipeline Phases

1. **Discovery**: Detect ecosystems and build repo manifests
2. **SBOM Generation**: Syft generates CycloneDX SBOMs
3. **Vulnerability Scanning**: Grype + OSV Scanner + Trivy analysis
4. **Matrix Building**: Cross-repo dependency and upgrade matrices
5. **Remediation** (optional): Apply ecosystem-specific fixes with rollback safety
6. **Documentation**: Generate comprehensive system and per-repo docs

## Output

Each run generates:

**System-level** (in `--output` directory):
- `SYSTEM_ARCHITECTURE.md` — System overview with C4 diagrams
- `DEPENDENCY_MATRIX.md` — Cross-repo dependency table
- `UPGRADE_MATRIX.md` — Vulnerability fix recommendations
- `PIPELINE_SEQUENCE.md` — Execution flow diagrams

**Per-repository** (in `<repo>/docs/`):
- `SBOM.md` — Software bill of materials
- `VULNERABILITY_REPORT.md` — CVE details and severity
- `UPGRADE_PLAN.md` — Specific upgrades for this repo
- `ARCHITECTURE.md` — Repository component diagram
- `CODING_GUIDELINES.md` — Detected conventions
- `SEQUENCE_DIAGRAMS.md` — Remediation flowcharts
- `TEST_CASES.md` — Test templates and matrix

## Configuration

Environment variables or CLI flags:

```bash
depshield \
  --repos ./repo1 ./repo2 \
  --output ./depshield-output \
  --dry-run \                    # Default: True
  --apply \                      # Apply mutations
  --verbose \                    # Debug logging
  --ecosystems jvm python        # Filter ecosystems
```

For detailed configuration options and examples, see:
- [spec.md — CLI Specifications](./spec.md#13-cli-specifications)
- [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md)

## Development

```bash
# Install dev dependencies
make dev

# Run tests
make test

# Lint and format
make lint
make format

# Build Docker image
make docker-build
```

## CI/CD Integration

### GitHub Actions

Copy `ci-templates/github-actions.yml` to `.github/workflows/depshield.yml`:

```yaml
name: DepShield
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install depshield
      - run: depshield --repos ./ --output ./reports --dry-run
      - uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: reports/
```

### GitLab CI

Copy `ci-templates/gitlab-ci.yml` to `.gitlab-ci.yml` and adjust for your repos.

## Architecture

See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) for detailed system design, data flow, and extensibility.

**Project Structure**:
```
depshield/                           # Core vulnerability pipeline
├── cli.py                         # Click CLI entry point
├── config.py                      # Pydantic configuration
├── pipeline.py                    # Phase orchestrator (6 phases)
├── discovery.py                   # Repo discovery & ecosystem detection
├── models.py                      # Data models
├── scanners/                      # Syft, Grype, OSV, Trivy
├── remediation/                   # OpenRewrite, pip, npm, go, cargo
├── matrix/                        # Dependency & upgrade matrices
└── reporters/                     # SBOM, vuln, arch, diagrams, guidelines, tests

ui/                                # Web dashboard
├── backend/                       # FastAPI application
│   ├── main.py                    # App factory
│   ├── store.py                   # In-memory state store
│   ├── models.py                  # API models
│   └── routes/                    # API endpoints
├── frontend/                      # React + TypeScript
│   ├── src/components/            # React components
│   ├── src/api.ts                 # API client
│   └── src/types.ts               # TypeScript types
└── README.md                      # Dashboard documentation

docs/                              # Documentation
├── ARCHITECTURE.md                # System design (detailed)
└── GETTING_STARTED.md             # Setup tutorial
```

**See also**:
- [spec.md](./spec.md) for functional and technical specifications
- [claude.md](./claude.md) for detailed module descriptions and development patterns

## Security

- **No Root Required**: Runs unprivileged except where necessary (e.g., Docker build)
- **Rollback Safety**: Git stash before remediation; automatic rollback on build/test failure
- **Dry-Run First**: Default mode generates reports without mutations
- **Explicit Apply**: Requires `--no-dry-run --apply` flags to modify code

**Core Security Principles**:
- Safety is non-negotiable — Every action is reversible
- Transparency is required — Users always know what changed
- No code execution — Scanning only, no shell script execution
- No data exfiltration — All operations are local

For detailed security specifications and philosophy, see:
- [soul.md — Core Principles](./soul.md#1-safety-first-always)
- [spec.md — Security Specifications](./spec.md#5-security-specifications)
- [claude.md — Security Considerations](./claude.md#security-considerations)

## Roadmap

See [plan.md](./plan.md) for detailed roadmap with phases and milestones.

**Phase 2 (Next 6 months)**:
- [ ] Community launch and adoption
- [ ] Production hardening
- [ ] Enterprise features (auth, audit logs, persistence)

**Phase 3+ (12+ months)**:
- [ ] Advanced remediation (custom recipes, approval workflows)
- [ ] ML-based risk scoring
- [ ] Policy engine and compliance automation
- [ ] SAAS offering and marketplace

See the [Roadmap section in plan.md](./plan.md#phase-2-community--adoption-q1-q2-2025) for detailed milestones.

## Contributing

Contributions welcome! Please:
1. Read [claude.md](./claude.md) (development guide)
2. Fork the repo
3. Create a feature branch
4. Add tests for new functionality
5. Submit a PR with description

See [claude.md](./claude.md#when-to-ask-for-help) for guidance on asking for help.

## License

Apache 2.0 — See LICENSE file

## Learn More

### For Different Audiences

**🧑‍💻 Developers & Contributors**
- Start with [QUICKSTART.md](./QUICKSTART.md) for setup
- Read [claude.md](./claude.md) for development guidelines
- Check [spec.md](./spec.md) for technical details

**📊 Product & Leadership**
- Read [intent.md](./intent.md) for vision and goals
- Review [plan.md](./plan.md) for roadmap and projections
- Check [soul.md](./soul.md) for core values and philosophy

**🔒 Security & Compliance**
- Review [spec.md](./spec.md) for security specifications
- Check [soul.md](./soul.md) for safety principles
- Read [intent.md](./intent.md) for security guarantees

**🎯 First-Time Users**
- Start with [QUICKSTART.md](./QUICKSTART.md) (5 minutes)
- Try the examples in [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md)
- Run `depshield --help` for CLI help

### Key Docs by Question

| Question | Document |
|----------|----------|
| "Why does DepShield exist?" | [intent.md](./intent.md) |
| "How does it work?" | [spec.md](./spec.md) |
| "What's the roadmap?" | [plan.md](./plan.md) |
| "What are the values?" | [soul.md](./soul.md) |
| "How do I contribute?" | [claude.md](./claude.md) |
| "Where do I start?" | [QUICKSTART.md](./QUICKSTART.md) |
| "How do I set it up?" | [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md) |
| "What was built?" | [COMPLETE.md](./COMPLETE.md) |
| "How do I navigate all docs?" | [SPECS.md](./SPECS.md) |

## Support

- **Questions?** Check [QUICKSTART.md](./QUICKSTART.md) or [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md)
- **Found a bug?** [Open an issue](https://github.com/yourusername/depshield/issues)
- **Want to contribute?** Read [claude.md](./claude.md#when-to-ask-for-help)
- **Need more info?** Check [SPECS.md](./SPECS.md) for complete documentation index
- **Understand the project?** Read [intent.md](./intent.md) and [soul.md](./soul.md)
