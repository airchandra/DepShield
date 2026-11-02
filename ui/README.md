# DepShield Dashboard UI

A comprehensive web interface for the DepShield vulnerability remediation pipeline.

## Architecture

```
ui/
├── backend/                 # FastAPI application
│   ├── main.py             # App factory, CORS, routes
│   ├── store.py            # In-memory run state store
│   ├── models.py           # Pydantic API models
│   └── routes/
│       ├── runs.py         # Run CRUD operations
│       ├── logs.py         # SSE log streaming
│       ├── vulns.py        # Vulnerability queries
│       ├── matrix.py       # Dependency & upgrade matrices
│       └── reports.py      # Markdown report serving
└── frontend/               # React + TypeScript + Vite
    ├── src/
    │   ├── main.tsx        # Entry point
    │   ├── App.tsx         # Router & layout
    │   ├── types.ts        # TypeScript types
    │   ├── api.ts          # API client
    │   ├── components/     # React components
    │   │   ├── RunForm.tsx          # Form to start scan
    │   │   ├── RunList.tsx          # List all runs
    │   │   ├── RunDetail.tsx        # Run summary + logs
    │   │   ├── ScanLog.tsx          # SSE log viewer
    │   │   ├── VulnTable.tsx        # Filterable CVE table
    │   │   ├── MatrixView.tsx       # Dependency & upgrade matrices
    │   │   ├── ReportViewer.tsx     # Markdown report renderer
    │   │   ├── SeverityBadge.tsx    # Severity color badge
    │   │   └── EcosystemChip.tsx    # Ecosystem tag
    │   └── hooks/          # Custom React hooks
    │       ├── useRun.ts            # Poll run status
    │       └── useLogs.ts           # SSE log streaming
    ├── index.html
    ├── vite.config.ts
    ├── tailwind.config.js
    ├── postcss.config.js
    └── package.json
```

## Setup & Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd ui/backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run dev server
uvicorn main:app --reload --port 8000
```

The backend starts on `http://localhost:8000` with API docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd ui/frontend

# Install dependencies
npm install

# Run dev server (proxies /api to backend)
npm run dev
```

The frontend starts on `http://localhost:5173`.

### Run Both Simultaneously

```bash
# Terminal 1: Backend
cd ui/backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd ui/frontend
npm run dev

# Open browser to http://localhost:5173
```

## API Endpoints

### Runs
- `POST /api/runs` — Create a new scan run
- `GET /api/runs` — List all runs
- `GET /api/runs/{id}` — Get full run details

### Logs
- `GET /api/runs/{id}/logs` — Server-Sent Events stream of log lines

### Vulnerabilities
- `GET /api/runs/{id}/vulnerabilities` — Get all vulns with optional filters
  - Query params: `?severity=critical&repo=api&sort=cvss_score`

### Matrices
- `GET /api/runs/{id}/matrix/dependency` — Dependency matrix rows
- `GET /api/runs/{id}/matrix/upgrade` — Upgrade matrix rows

### Reports
- `GET /api/runs/{id}/repos/{name}/reports/{filename}` — Per-repo markdown report
- `GET /api/runs/{id}/system-reports/{filename}` — System-level markdown report

### Health
- `GET /api/health` — Health check

## Frontend Routes

| Route | Component | Purpose |
|-------|-----------|---------|
| `/` | `RunList` + `RunForm` | Home: all runs + new scan form |
| `/runs/:id` | `RunDetail` | Run summary, status, live logs |
| `/runs/:id/vulns` | `VulnTable` | Filterable vulnerability table |
| `/runs/:id/matrix` | `MatrixView` | Dependency & upgrade matrices |
| `/runs/:id/reports/:repo` | `ReportViewer` | View markdown reports |

## Features

### Run Management
- Create new scans with custom repo list and options
- View all past runs with status and summary
- Real-time scan progress via live log stream
- Run history with timestamps

### Vulnerability Exploration
- Complete CVE table with severity, CVSS, current/fixed versions
- Filter by severity, repository, ecosystem
- Sort by severity, CVSS score, or package name
- Quick links to CVE advisories

### Dependency Analysis
- **Dependency Matrix**: Which packages are used in which repos
- **Upgrade Matrix**: Recommended safe versions for each package
- Conflict detection: Identify version mismatches across repos
- CVSS scoring and severity levels

### Report Viewing
- View auto-generated markdown reports in the browser
- Per-repository SBOM, vulnerability reports, architecture diagrams
- System-level architecture overview and matrices
- **Mermaid diagram rendering** for:
  - C4 context and component diagrams
  - Sequence diagrams
  - Flowchart visualizations

### Responsive Design
- Tailwind CSS styling
- Mobile-friendly layout
- Dark mode support (via Tailwind config)
- Accessibility-first component design

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | React 18 + TypeScript | Type-safe, modern React |
| Frontend Build | Vite | Fast dev server, optimized builds |
| Styling | Tailwind CSS | Utility-first, no extra CSS |
| Routing | React Router v6 | Standard routing |
| Markdown | react-markdown + GFM | Renders GitHub Flavored Markdown |
| Diagrams | Mermaid | SVG diagrams from markdown |
| Backend | FastAPI | Async, built-in OpenAPI docs |
| Streaming | SSE (Server-Sent Events) | Live log streaming |
| State | In-memory (RunStore) | No DB needed for MVP |

## Building for Production

### Backend
```bash
cd ui/backend
# Just run with uvicorn (or gunicorn for production)
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend
```bash
cd ui/frontend
npm run build
# Outputs to dist/
# Served by FastAPI static files middleware
```

### Docker
```bash
# Build image
docker build -t depshield-ui:latest .

# Run
docker run -p 8000:8000 depshield-ui:latest
```

## Development Notes

### Adding a New Component
1. Create `.tsx` file in `src/components/`
2. Implement React component with TypeScript
3. Import in `App.tsx` router if it's a page component
4. Use `api.*` methods from `src/api.ts` for server calls

### Extending the Backend
1. Create new route file in `ui/backend/routes/`
2. Define Pydantic models in `ui/backend/models.py`
3. Include router in `ui/backend/main.py` with `app.include_router()`

### Styling
- Use Tailwind classes for all styling (no custom CSS unless necessary)
- Color custom severity levels in `tailwind.config.js`
- Responsive breakpoints: `sm`, `md`, `lg`, `xl`, `2xl`

## Future Enhancements

- [ ] User authentication & authorization
- [ ] SQLite backend for run history persistence
- [ ] Export reports as PDF
- [ ] Real-time WebSocket updates instead of polling
- [ ] Dark mode toggle
- [ ] Custom remediation recipe builder
- [ ] Integration with GitHub/GitLab for PR creation
- [ ] Scheduled scans configuration
- [ ] Webhook notifications

## Troubleshooting

### CORS errors
- Check that backend is running on `:8000` and frontend proxy is configured in `vite.config.ts`
- In production, disable CORS in `main.py` if serving frontend from same origin

### Log stream closes early
- SSE has a 30-60 second timeout in some proxies; in production use WebSockets
- Check `RUN_COMPLETE` message in EventSource to know when run is done

### Markdown doesn't render
- Ensure `react-markdown` and `remark-gfm` are installed
- Check browser console for parsing errors
- Markdown files must be valid UTF-8

## License

Apache 2.0 — Same as DepShield
