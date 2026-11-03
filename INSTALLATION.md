# DepShield Installation Guide

## System Requirements

- **Python:** 3.11 or higher
- **Node.js:** 16+ (for web dashboard)
- **Package Manager:** pip or pipx
- **OS:** macOS, Linux, or WSL on Windows

---

## Installation Methods

### Method 1: Virtual Environment (Recommended)

Use a Python virtual environment to avoid system package conflicts:

```bash
# Clone the repository
git clone https://github.com/airchandra/DepShield.git
cd DepShield

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install in development mode
pip install -e .

# Verify installation
depshield --help
```

### Method 2: pipx (Isolated Installation)

Install DepShield in an isolated environment without affecting system Python:

```bash
# Install pipx (if not already installed)
brew install pipx  # macOS
# or
apt-get install pipx  # Ubuntu/Debian

# Install DepShield
pipx install -e .

# Verify installation
depshield --help
```

### Method 3: Homebrew (macOS Only)

If you want to contribute back a Homebrew formula:

```bash
# Future: Once Homebrew formula is created
brew install depshield
depshield --help
```

---

## Troubleshooting Installation

### Issue: "externally-managed-environment"

**Problem:**
```
error: externally-managed-environment
× This environment is externally managed
```

**Solution:** Use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Or use pipx:

```bash
pipx install -e .
```

### Issue: "No module named 'depshield'"

**Problem:** Installation didn't complete successfully

**Solution:**
```bash
# Reinstall with verbose output
pip install -e . -v

# Check installation
pip show depshield

# If not found, try:
python3 -m pip install -e .
```

### Issue: "Python 3.11+ required"

**Problem:** Using Python 3.10 or older

**Solution:**
```bash
# Check Python version
python3 --version

# If older than 3.11, install newer version:
brew install python@3.12  # macOS
# or
apt-get install python3.12  # Ubuntu

# Use specific version
python3.12 -m venv venv
source venv/bin/activate
pip install -e .
```

### Issue: "command not found: depshield"

**Problem:** CLI not in PATH

**Solution:**
```bash
# Check if installed
pip show depshield

# Try running as module
python3 -m depshield.cli --help

# Verify venv is activated
which python3
which pip

# Reinstall
pip install -e . --force-reinstall
```

---

## Post-Installation Setup

### 1. Install Required Scanning Tools

DepShield uses external tools for vulnerability scanning. Install them:

**macOS:**
```bash
# Install via Homebrew
brew install syft grype trivy

# Install osv-scanner (Go required)
go install github.com/google/osv-scanner@latest
```

**Ubuntu/Debian:**
```bash
# Install via apt
apt-get update
apt-get install syft grype trivy

# Install osv-scanner (Go required)
go install github.com/google/osv-scanner@latest
```

**Verify Installation:**
```bash
which syft grype osv-scanner trivy
# Should show paths to all 4 tools
```

### 2. Verify All Dependencies

```bash
# Check Python packages
pip list | grep -E "depshield|fastapi|pydantic|click"

# Check system tools
syft --version
grype --version
osv-scanner --version
trivy --version
```

### 3. Run CLI Test

```bash
depshield --help

# Should output:
# Usage: depshield [OPTIONS]
# 
#   DepShield — Zero-critical-vulnerabilities pipeline.
#   ...
```

---

## Installing Web Dashboard Dependencies

### Backend

```bash
cd ui/backend
pip install -r requirements.txt

# Or if using virtual env:
source ../../venv/bin/activate  # If needed
pip install -r requirements.txt
```

### Frontend

```bash
cd ui/frontend

# Install Node dependencies
npm install

# Or use yarn
yarn install
```

---

## Running DepShield

### CLI

```bash
# Basic scan (dry-run mode - no changes)
depshield --repos /path/to/repo --dry-run

# With verbose output
depshield --repos /path/to/repo --dry-run --verbose

# Specific ecosystems only
depshield --repos /path/to/repo --ecosystems jvm python

# Multiple repositories
depshield --repos ./repo1 ./repo2 ./repo3 --dry-run
```

### Web Dashboard

**Terminal 1 - Backend:**
```bash
cd ui/backend
source ../../venv/bin/activate  # If using venv
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd ui/frontend
npm install
npm run dev
```

**Access Dashboard:**
```
http://localhost:5173
```

---

## Development Installation

For contributors who want to modify the code:

```bash
# Clone repository
git clone https://github.com/airchandra/DepShield.git
cd DepShield

# Create development virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install

# Run tests
pytest tests/ -v

# Run linting
ruff check depshield/

# Format code
black depshield/ ui/frontend/src/
```

---

## Environment Variables

Set these before running:

```bash
# CLI Configuration
export DEPSHIELD_REPOS="./repo1,./repo2"
export DEPSHIELD_OUTPUT_DIR="./reports"
export DEPSHIELD_DRY_RUN=true
export DEPSHIELD_VERBOSE=false
export DEPSHIELD_ECOSYSTEMS="jvm,python,javascript,go,rust"

# Backend Configuration
export ALLOWED_ORIGINS="http://localhost:3000,http://localhost:5173"
```

---

## Docker Installation

If you prefer Docker:

```bash
# Build image
docker build -t depshield:latest -f docker/Dockerfile .

# Run container
docker run -v /path/to/repos:/repos \
           -v /path/to/output:/output \
           depshield:latest \
           depshield --repos /repos --output /output --dry-run
```

---

## Verification Checklist

After installation, verify everything works:

```bash
# ✅ Python version
python3 --version  # Should be 3.11+

# ✅ DepShield installed
depshield --version  # Or: depshield --help

# ✅ Scanning tools available
which syft grype osv-scanner trivy

# ✅ Backend dependencies
python3 -c "import fastapi; import uvicorn; print('✅ FastAPI OK')"

# ✅ Frontend dependencies
node --version  # Should be 16+
npm --version

# ✅ Test scan (no changes)
depshield --repos . --dry-run --verbose
```

---

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Reinstall package
pip install -e . --force-reinstall

# Uninstall
pip uninstall depshield

# Update dependencies
pip install -e . --upgrade

# Check installed version
pip show depshield

# View installed packages
pip list
```

---

## Next Steps

1. ✅ Install DepShield: `pip install -e .`
2. ✅ Install scanning tools: `brew install syft grype trivy`
3. ✅ Verify installation: `depshield --help`
4. ✅ Test with sample repo: `depshield --repos . --dry-run`
5. ✅ Run tests: `python3 test_fixes.py`
6. ✅ Start dashboard: See "Running DepShield" section

---

## Support

If installation fails:

1. Check Python version: `python3 --version`
2. Use virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install with verbose output: `pip install -e . -v`
4. Check our troubleshooting guide above
5. Review README.md for additional help

---

**You're all set! DepShield is ready to use.** 🚀
