# DepShield Quick Start - After Code Review

## ✅ What's Been Done

- Deep code review: 18 issues identified
- Critical fixes applied: 10 bugs fixed
- Comprehensive documentation created
- Test suite provided
- All changes committed to GitHub

---

## 🚀 What You Need To Do

### 1. Install DepShield
```bash
git clone https://github.com/airchandra/DepShield.git
cd DepShield
pip install -e .
```

### 2. Verify Installation
```bash
depshield --help
```

Should show DepShield CLI with all options.

### 3. Install Required Scanning Tools
Choose based on your OS:

**macOS:**
```bash
brew install syft grype trivy
go install github.com/google/osv-scanner@latest
```

**Ubuntu/Debian:**
```bash
apt-get install syft grype trivy
go install github.com/google/osv-scanner@latest
```

**Verify tools installed:**
```bash
which syft grype osv-scanner trivy
```

### 4. Run a Test Scan
```bash
# Create or use an existing repository
depshield --repos /path/to/your/repo --dry-run --verbose

# This will:
# - Detect ecosystems (Maven, npm, pip, go, cargo)
# - Generate SBOM with Syft
# - Scan for vulnerabilities (Grype, OSV, Trivy)
# - Generate comprehensive reports
# - NOT make any changes (dry-run mode)
```

### 5. Try the Web Dashboard
```bash
# Terminal 1: Start Backend
cd ui/backend
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2: Start Frontend
cd ui/frontend
npm install
npm run dev

# Visit http://localhost:5173
```

### 6. Run the Fix Verification Test
```bash
python3 test_fixes.py
```

Should show tests passing/failing based on installed dependencies.

---

## 📋 Files To Review

1. **CODE_REVIEW_SUMMARY.md** (Start here!)
   - Overview of code review and all fixes
   - Step-by-step deployment guide
   - Troubleshooting section

2. **FIXES_APPLIED.md**
   - Technical details of each fix
   - Before/after code examples
   - Remaining known issues

3. **README.md**
   - User guide and features
   - Architecture overview
   - Configuration options

4. **docs/DIAGRAMS.md**
   - 11 professional architecture diagrams
   - System design at multiple levels
   - Data flow visualizations

---

## ⚙️ Environment Variables

Set these before running:

```bash
# For CLI
export DEPSHIELD_REPOS="./repo1,./repo2"
export DEPSHIELD_DRY_RUN=true
export DEPSHIELD_VERBOSE=false

# For Backend (if not localhost)
export ALLOWED_ORIGINS="http://your-domain:3000"
```

---

## ✅ Success Checklist

- [ ] Cloned repository
- [ ] Installed with `pip install -e .`
- [ ] `depshield --help` works
- [ ] Installed scanning tools (syft, grype, trivy, osv-scanner)
- [ ] Successfully ran test scan with `--dry-run`
- [ ] Web dashboard starts without errors
- [ ] Can view dashboard at http://localhost:5173
- [ ] Read CODE_REVIEW_SUMMARY.md

---

## 🔍 If Something Doesn't Work

**CLI not found after pip install:**
```bash
which depshield
# If empty, try:
python3 -m depshield.cli --help
```

**Import errors:**
```bash
# Reinstall in development mode
pip install -e . --force-reinstall
```

**Backend won't start:**
```bash
cd ui/backend
pip install -r requirements.txt
# Make sure Python 3.11+ is being used
python3 --version
```

**Frontend won't start:**
```bash
cd ui/frontend
npm install
# Make sure Node 16+ is installed
node --version
```

**Scanners not found:**
```bash
# Verify installation
which syft
which grype
# If missing, install using your OS package manager
```

---

## 🎯 Next Goals

After everything works:

1. **Test with real repositories** - Scan your actual codebases
2. **Customize for your needs** - Adjust ecosystems, add custom scanners
3. **Deploy to CI/CD** - Use GitHub Actions or GitLab CI templates
4. **Address remaining issues** - See FIXES_APPLIED.md for low-priority items

---

## 📞 Troubleshooting

Detailed troubleshooting is in **CODE_REVIEW_SUMMARY.md** under "Support & Troubleshooting"

Key issues:
- Missing dependencies → `pip install -e .`
- Scanners not found → Install with your OS package manager
- Backend can't connect to frontend → Set `ALLOWED_ORIGINS`
- Logger issues → Verify Python 3.11+ is installed

---

## 📊 What's Been Fixed

All critical issues that prevented running:
1. ✅ Missing backend dependencies (FastAPI, Uvicorn)
2. ✅ Wrong Pydantic configuration syntax
3. ✅ Broken command parsing for complex arguments
4. ✅ Wrong severity comparison logic
5. ✅ Unsafe CVSS parsing in scanners
6. ✅ Logger name mismatch between modules
7. ✅ Overly permissive CORS configuration
8. ✅ Removed unused imports
9. ✅ Fixed frontend branding
10. ✅ Fixed GitHub URL

---

**You're all set! Follow the steps above to get DepShield running. 🚀**
