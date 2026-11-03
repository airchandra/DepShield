import { BrowserRouter, Routes, Route } from 'react-router-dom'
import RunForm from './components/RunForm'
import RunList from './components/RunList'
import RunDetail from './components/RunDetail'
import VulnTable from './components/VulnTable'
import MatrixView from './components/MatrixView'
import ReportViewer from './components/ReportViewer'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900">
                🔒 DepShield
              </h1>
              <p className="text-sm text-gray-600">Vulnerability Remediation Dashboard</p>
            </div>
          </div>
        </header>

        {/* Main */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/runs/:id" element={<RunDetail />} />
            <Route path="/runs/:id/vulns" element={<VulnTable />} />
            <Route path="/runs/:id/matrix" element={<MatrixView />} />
            <Route path="/runs/:id/reports/:repo" element={<ReportViewer />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-gray-100 border-t border-gray-200 mt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-sm text-gray-600">
            <p>DepShield © 2024 • <a href="https://github.com/airchandra/DepShield" className="text-blue-600 hover:underline">GitHub</a></p>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  )
}

function Home() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-1">
        <RunForm />
      </div>
      <div className="lg:col-span-2">
        <RunList />
      </div>
    </div>
  )
}
