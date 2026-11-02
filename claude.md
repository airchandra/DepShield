# claude.md — DepShield Development Guide

Instructions for Claude Code when working with the DepShield codebase.

---

## Project Overview

**DepShield** is a vulnerability remediation pipeline for distributed systems. It scans multi-repo systems, analyzes vulnerabilities, and safely remediates them.

**Structure**:
- `./depshield/` — Core Python pipeline (33 modules)
- `./ui/` — Web dashboard (FastAPI backend + React frontend)
- `./tests/` — Unit tests
- `./docs/` — Documentation
- `./docker/` — Docker configs
- `./ci-templates/` — GitHub Actions & GitLab CI

**Key Files**:
- `intent.md` — Project vision & goals
- `spec.md` — Technical specifications
- `plan.md` — Roadmap & milestones
- `soul.md` — Design philosophy
- `README.md` — User guide

---

## Development Principles

### 1. Safety First
- Never write code that breaks user's repositories
- All mutations must be reversible (use git stash)
- Validate inputs before processing
- Test with fixtures before assuming it works

### 2. Type Safety
- Use Pydantic models for all data validation
- Use TypeScript on frontend
- Define clear data contracts
- Avoid `any` types

### 3. Transparency
- Log what the tool is doing
- Show exactly what changed
- Document why decisions were made
- Admit limitations

### 4. Simplicity
- Code should be readable first
- Prefer explicit over implicit
- Name variables clearly
- Avoid clever tricks

### 5. Testing Matters
- Unit test business logic
- Integration test pipelines
- Test with real fixtures
- Don't test framework code

---

## Code Style & Conventions

### Python

**Imports**:
```python
# Standard library first
import asyncio
import logging
from pathlib import Path

# Third-party
from pydantic import BaseModel

# Local
from depshield.models import Vulnerability
from depshield.scanners.base import BaseScanner
```

**Naming**:
- Classes: `PascalCase` (e.g., `SyftScanner`)
- Functions: `snake_case` (e.g., `build_matrix`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_WORKERS`)
- Private: `_leading_underscore`

**Type Hints**:
```python
def remediate(self, dry_run: bool = True) -> RemediationResult:
    """Short description.
    
    Args:
        dry_run: Whether to apply changes
        
    Returns:
        RemediationResult with status
    """
```

**Docstrings**:
- One-line for simple functions
- Multi-line (Google style) for complex functions
- Focus on *why*, not *what* (code shows what)

**Logging**:
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Starting scan of {repo.name}")
logger.warning(f"SBOM not found for {repo.name}")
logger.error(f"Remediation failed: {error}")
```

### React/TypeScript

**Naming**:
- Components: `PascalCase` (e.g., `VulnTable.tsx`)
- Hooks: `useXxx` (e.g., `useRun.ts`)
- Types: `PascalCase` (e.g., `RunSummary`)
- Functions/constants: `camelCase`

**Components**:
```typescript
interface Props {
  runId: string
  onUpdate?: () => void
}

export default function VulnTable({ runId, onUpdate }: Props) {
  // Component logic
  return <div>...</div>
}
```

**Styles**:
- Use Tailwind classes exclusively
- No custom CSS unless unavoidable
- Mobile-first (small screens → responsive)
- Color scheme: Use severity colors from config

### Git Conventions

**Commits**:
```
scope: one-line summary

Longer explanation if needed.
- Bullet point details
- More context

Fixes #123
```

**Scope** (before colon):
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `docs:` Documentation
- `test:` Test addition/fix
- `ci:` CI/CD changes
- `perf:` Performance optimization

---

## Working With the Codebase

### Adding a New Ecosystem

1. **Update `depshield/models.py`**:
   ```python
   class Ecosystem(str, Enum):
       # Add new ecosystem
       MY_LANG = "mylang"
   ```

2. **Create scanner** (`depshield/scanners/mylang.py`):
   ```python
   from depshield.scanners.base import BaseScanner
   
   class MyLangScanner(BaseScanner):
       def scan(self) -> ScanResult:
           # Detect manifest, run scanner, parse output
           pass
   ```

3. **Create remediator** (`depshield/remediation/mylang_upgrader.py`):
   ```python
   from depshield.remediation.base import BaseRemediator
   
   class MyLangRemediator(BaseRemediator):
       def remediate(self, dry_run: bool = True) -> RemediationResult:
           # Upgrade dependencies safely
           pass
   ```

4. **Register in** `depshield/discovery.py`:
   ```python
   def _detect_ecosystems(repo_path: Path) -> List[Ecosystem]:
       if (repo_path / "manifest.toml").exists():
           ecosystems.append(Ecosystem.MY_LANG)
   ```

5. **Register in** `depshield/pipeline.py`:
   ```python
   def _get_remediator(self, repo: RepoManifest, ecosystem: Ecosystem):
       if ecosystem == Ecosystem.MY_LANG:
           return MyLangRemediator(repo, self.config)
   ```

6. **Add tests** (`tests/test_mylang.py`)
7. **Update docs** (mention new ecosystem)

### Adding a Feature

**Small feature** (< 200 lines):
1. Create feature in existing module
2. Add unit test
3. Update relevant doc
4. Submit PR

**Medium feature** (200-500 lines):
1. Check with issue/discussion first
2. Design in comment before coding
3. Add unit + integration tests
4. Update docs + README
5. Submit PR with demo

**Large feature** (> 500 lines):
1. Open issue describing feature
2. Get feedback on approach
3. Design document (in issue)
4. Implement with tests
5. Submit PR with detailed description

### Debugging the Pipeline

**Enable verbose logging**:
```bash
depshield --repos . --verbose
```

**Run individual phases**:
```python
# In Python REPL
from depshield.discovery import RepositoryDiscovery
repos = RepositoryDiscovery.discover_repos(["."])
```

**Inspect intermediate outputs**:
```python
# SBOM files live in ./depshield-output/sbom/
# Vulnerability results in ./depshield-output/grype/
import json
with open("sbom.json") as f:
    sbom = json.load(f)
```

**Test with fixtures**:
```bash
cd tests/fixtures/jvm-app
depshield --repos . --dry-run --verbose
```

### Modifying the API

**Adding an endpoint**:
1. Add Pydantic model to `ui/backend/models.py`
2. Create route file `ui/backend/routes/xxx.py`
3. Include router in `ui/backend/main.py`
4. Update API client `ui/frontend/src/api.ts`
5. Update frontend to use new endpoint

**Breaking API changes**:
- Should be rare (design carefully)
- Must be documented
- Version change (MAJOR bump)
- Update both frontend and CLI

### Dashboard Development

**Running locally**:
```bash
# Terminal 1: Backend
cd ui/backend
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2: Frontend
cd ui/frontend
npm install
npm run dev

# http://localhost:5173
```

**Adding a component**:
1. Create `src/components/MyComponent.tsx`
2. Define Props interface
3. Use API from `src/api.ts`
4. Add to router in `App.tsx`
5. Add tests (future)

**Styling**:
- Use Tailwind classes
- No CSS files unless absolutely necessary
- Check `tailwind.config.js` for custom colors
- Mobile-first responsive design

---

## Common Tasks

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific test
pytest tests/test_discovery.py::test_discover_jvm_repo -v

# With coverage
pytest tests/ --cov=harness
```

### Building Docker
```bash
docker build -t depshield:latest .
docker run -v ./repos:/repos depshield:latest
```

### Creating a Release
```bash
# Update version in pyproject.toml
# Update CHANGELOG
git tag v1.2.3
git push origin v1.2.3
# CI builds and pushes to PyPI
```

### Documentation

**When to write docs**:
- New ecosystem support
- New major feature
- API changes
- Configuration options
- Troubleshooting/gotchas

**Where docs live**:
- `README.md` — User guide (most important)
- `docs/ARCHITECTURE.md` — System design
- `docs/GETTING_STARTED.md` — Step-by-step
- Code comments — Only for *why*, not *what*

---

## Performance Considerations

### Scanning Performance
- Don't block on network calls → use async
- Parallel scanning across repos (but not within)
- Cache SBOM results if re-scanning same repo
- Stream large vulnerability lists (don't load all in memory)

### Frontend Performance
- Lazy load routes (React Router code splitting)
- Virtualize long lists (if vuln table > 1000 rows)
- Debounce filter inputs
- Memoize expensive computations

### Database (when added)
- Index on run.id, run.status, created_at
- Partition old runs
- Archive logs separately

---

## Security Considerations

### Never Do This
- ❌ Run untrusted code (no `eval`, `exec`, subprocess with shell=True)
- ❌ Log credentials/secrets
- ❌ Store passwords in code
- ❌ Trust user input (validate everything)
- ❌ Assume file paths are safe (use `Path` not string concatenation)

### Always Do This
- ✅ Validate all inputs (Pydantic models)
- ✅ Use git for all mutations (reversible)
- ✅ Run subprocess with explicit arguments (no shell=True)
- ✅ Check file permissions before reading
- ✅ Assume the worst case (malicious input)

---

## Decision Framework

When facing a design decision:

**Ask yourself**:
1. Is this safe? (Would this break user's code?)
2. Is this transparent? (Would users understand why?)
3. Is this simple? (Can a new user figure it out?)
4. Is this tested? (Do we know it works?)
5. Is this documented? (Will future-you understand?)

If any answer is "no", reconsider the design.

---

## When to Ask for Help

- **Uncertain about direction**: Open an issue with `[RFC]` tag
- **Stuck on a bug**: Write minimal reproduction, share it
- **Need design feedback**: Comment on related issue with proposal
- **Want to contribute**: Check CONTRIBUTING.md (future) or ask

---

## Useful Commands

```bash
# Install in development mode
pip install -e .

# Run CLI
depshield --repos . --dry-run --verbose

# Run tests with coverage
pytest tests/ --cov=harness --cov-report=html

# Linting
ruff check depshield/

# Type checking
mypy depshield/

# Format code
black depshield/ tests/

# Build Docker
docker build -t depshield:latest .

# Run docker
docker run -v $(pwd)/repos:/repos -v $(pwd)/output:/output depshield:latest

# Start development servers
cd ui && make dev
```

---

## Anti-Patterns to Avoid

### ❌ Code Smell: Silent Failures
```python
# Bad
try:
    result = scan()
except Exception:
    pass  # Hidden failure!

# Good
try:
    result = scan()
except Exception as e:
    logger.error(f"Scan failed: {e}")
    raise
```

### ❌ Code Smell: Type Unpredictability
```python
# Bad
def process(data):  # Could be anything!
    return data.upper()  # What if data is not a string?

# Good
def process(data: str) -> str:
    return data.upper()
```

### ❌ Code Smell: Hidden Complexity
```python
# Bad (what does this do?)
result = reduce(lambda x, y: x + (y[1] if y[2] > 5 else 0), items, 0)

# Good (clear intent)
high_value_items = [item for item in items if item.priority > 5]
total = sum(item.value for item in high_value_items)
```

---

## The Bottom Line

When working on DepShield, remember:

1. **Safety is non-negotiable** — Never break user code
2. **Transparency is required** — Users must understand what happened
3. **Simplicity is paramount** — Don't add complexity without reason
4. **Testing is not optional** — Especially for business logic
5. **Documentation is a feature** — Good docs are force multipliers

**If you're unsure about something, ask.** Better to clarify than to go down the wrong path.

---

*"Make it safe. Make it simple. Make it clear."* — DepShield Development Mantra
