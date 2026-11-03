# Getting Started with DepShield

## Prerequisites

- Python 3.11+
- Git
- Docker (optional, for containerized execution)
- System tools (mvn, npm, go, cargo, rustc — see Dockerfile for full list)

## Installation

### Option 1: pip (Recommended for local development)

```bash
git clone https://github.com/yourusername/depshield.git
cd depshield
pip install -e .
```

Verify installation:
```bash
depshield --help
```

### Option 2: Docker

```bash
# Build image
docker build -t depshield:latest -f docker/Dockerfile .

# Run
docker run -v ./repos:/repos -v ./output:/output depshield:latest \
  depshield --repos /repos --output /output --dry-run
```

### Option 3: Docker Compose

```bash
# Create output directory
mkdir -p depshield-output

# Run with compose
REPOS_PATH=./repos OUTPUT_PATH=./depshield-output docker-compose -f docker/docker-compose.yml up
```

## First Run

### 1. Scan a Single Repository

```bash
# Navigate to your project directory (containing pom.xml, package.json, go.mod, etc.)
cd /path/to/my-app

# Run a dry-run scan
depshield --repos ./ --output ./reports --dry-run --verbose
```

Output:
```
🚀 DepShield
Repositories: ./
Output: ./reports
Mode: DRY RUN
Ecosystems: jvm, python, javascript, go, rust

Phase 1: Repository Discovery
Phase 2: SBOM Generation
Phase 3: Vulnerability Scanning
Phase 4: Building Matrices
Phase 6: Generating Reports
✅ Pipeline completed successfully
Reports available at: ./reports
```

Check the output:
```bash
ls -la ./reports/
# SYSTEM_ARCHITECTURE.md
# DEPENDENCY_MATRIX.md
# UPGRADE_MATRIX.md
# PIPELINE_SEQUENCE.md

ls -la ./docs/
# SBOM.md
# VULNERABILITY_REPORT.md
# ARCHITECTURE.md
# CODING_GUIDELINES.md
# SEQUENCE_DIAGRAMS.md
# TEST_CASES.md
# UPGRADE_PLAN.md
```

### 2. Review Reports

Open the generated Markdown files:

```bash
# View vulnerability summary
cat reports/UPGRADE_MATRIX.md

# View system architecture
cat reports/SYSTEM_ARCHITECTURE.md

# View per-repo details
cat docs/VULNERABILITY_REPORT.md
```

### 3. Apply Remediation (Optional)

**⚠️ WARNING**: This will modify your code. Always commit before applying.

```bash
# Commit current state first
git add .
git commit -m "Pre-remediation checkpoint"

# Apply remediations
depshield --repos ./ --output ./reports --no-dry-run --apply --verbose

# Review changes
git diff
git status

# Test the build
mvn clean test  # or: npm test, go test ./..., cargo test, pytest

# If tests pass, commit the remediation
git add .
git commit -m "Security: Apply remediation for critical vulnerabilities"
```

## Multi-Repository Scan

```bash
depshield \
  --repos ./api ./frontend ./data-service \
  --output ./security-audit \
  --dry-run \
  --verbose
```

This scans all three repos and produces:
- `security-audit/SYSTEM_ARCHITECTURE.md` — inter-repo relationships
- `security-audit/DEPENDENCY_MATRIX.md` — shared dependencies
- `security-audit/UPGRADE_MATRIX.md` — upgrade recommendations across repos
- `api/docs/VULNERABILITY_REPORT.md` — per-repo vulnerabilities
- `frontend/docs/SBOM.md` — per-repo SBOM
- `data-service/docs/UPGRADE_PLAN.md` — per-repo upgrade plan

## Filtering by Ecosystem

```bash
# Only scan JVM and Python projects
depshield --repos ./ --output ./reports --dry-run --ecosystems jvm python

# Available: jvm, python, javascript, go, rust
```

## Verbose Logging

```bash
# Enable debug output
depshield --repos ./ --output ./reports --dry-run --verbose
```

## Common Workflows

### Scheduled Scans (GitHub Actions)

1. Copy `ci-templates/github-actions.yml` to `.github/workflows/depshield.yml`
2. Customize repo paths in the workflow
3. Push and watch Actions tab for scan results

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
set -e
depshield --repos ./ --dry-run
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Weekly Security Report

```bash
#!/bin/bash
# scripts/security-audit.sh
date=$(date +%Y-%m-%d)
depshield --repos ./apps ./services --output "./reports/$date" --dry-run
git add "./reports/$date"
git commit -m "security: weekly scan $date"
git push
```

## Troubleshooting

### "No repositories discovered"

Ensure the path contains a manifest file (pom.xml, package.json, go.mod, etc.):
```bash
ls -la /path/to/repo/
# Must have one of: pom.xml, build.gradle, package.json, go.mod, Cargo.toml, pyproject.toml
```

### "Syft not found"

Install system dependencies:
```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
```

Or use Docker:
```bash
docker build -t depshield:latest .
docker run -v ./repos:/repos depshield:latest depshield --repos /repos --dry-run
```

### Build/Test Failures After Remediation

Check logs:
```bash
depshield --repos ./ --output ./reports --no-dry-run --apply --verbose 2>&1 | tee remediation.log
```

The changes are automatically rolled back if build or tests fail. Review `remediation.log` for details.

## Next Steps

1. **Review Architecture Docs**: `reports/SYSTEM_ARCHITECTURE.md` explains your distributed system
2. **Check Vulnerabilities**: `docs/VULNERABILITY_REPORT.md` lists all CVEs and severity
3. **Plan Upgrades**: `docs/UPGRADE_PLAN.md` shows safe versions
4. **Apply Remediations**: Use `--apply` after review and testing
5. **Automate**: Set up CI/CD integration with GitHub Actions or GitLab CI
6. **Monitor**: Add scheduled scans to catch new vulnerabilities early

## Getting Help

```bash
depshield --help
```

See full documentation in `docs/` directory or visit the [GitHub repository](https://github.com/yourusername/depshield).
