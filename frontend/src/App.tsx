import { useEffect, useState } from 'react'
import { Activity, Database, Cpu, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react'

interface HealthState {
  status: string
  app: string
  environment: string
  database: string
  llm_provider: string
}

export default function App() {
  const [health, setHealth] = useState<HealthState | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const fetchHealth = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/health')
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`)
      }
      const data: HealthState = await res.json()
      setHealth(data)
    } catch (err: any) {
      setError(err.message || 'Failed to connect to backend server')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchHealth()
  }, [])

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between p-6">
      <header className="max-w-4xl mx-auto w-full flex justify-between items-center py-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20">
            L
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              The Lenny Growth Assistant
            </h1>
            <p className="text-xs text-slate-400">Forward Deployed Engineer Assessment</p>
          </div>
        </div>

        <button 
          onClick={fetchHealth}
          disabled={loading}
          className="flex items-center gap-2 text-xs font-medium bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-lg px-3 py-2 transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Status
        </button>
      </header>

      <main className="max-w-4xl mx-auto w-full my-auto py-12 flex flex-col items-center">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-6">
          <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
          PHASE 1: Foundation Ready
        </div>

        <h2 className="text-3xl font-extrabold text-center mb-3">
          System Infrastructure & Health Monitor
        </h2>
        <p className="text-slate-400 text-center max-w-lg text-sm mb-10">
          The foundation layer of The Lenny Growth Assistant is operational. Below is the live diagnostic state reported by the FastAPI backend.
        </p>

        {loading ? (
          <div className="flex items-center justify-center p-12 bg-slate-900/50 border border-slate-800 rounded-2xl w-full max-w-md">
            <RefreshCw className="w-6 h-6 text-indigo-400 animate-spin mr-3" />
            <span className="text-sm font-medium text-slate-300">Checking backend status...</span>
          </div>
        ) : error ? (
          <div className="bg-red-950/40 border border-red-800/60 rounded-2xl p-6 w-full max-w-md flex items-start gap-4">
            <AlertCircle className="w-6 h-6 text-red-400 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-red-300 text-sm">Backend Disconnected</h3>
              <p className="text-xs text-red-400/80 mt-1">{error}</p>
              <button 
                onClick={fetchHealth}
                className="mt-3 text-xs text-red-300 underline font-medium hover:text-white"
              >
                Retry connection
              </button>
            </div>
          </div>
        ) : health ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
            {/* API Status Card */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all">
              <div className="flex justify-between items-start mb-4">
                <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                  <Activity className="w-5 h-5" />
                </div>
                <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <CheckCircle2 className="w-3 h-3" /> {health.status.toUpperCase()}
                </span>
              </div>
              <h3 className="font-semibold text-sm text-slate-200">Backend API</h3>
              <p className="text-xs text-slate-400 mt-1">FastAPI status endpoint</p>
              <div className="mt-4 pt-3 border-t border-slate-800/80 flex justify-between text-xs">
                <span className="text-slate-500">Environment</span>
                <span className="font-mono text-slate-300">{health.environment}</span>
              </div>
            </div>

            {/* Database Status Card */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all">
              <div className="flex justify-between items-start mb-4">
                <div className={`p-2 rounded-lg ${health.database === 'connected' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'}`}>
                  <Database className="w-5 h-5" />
                </div>
                <span className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full ${
                  health.database === 'connected' 
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                }`}>
                  {health.database === 'connected' ? (
                    <><CheckCircle2 className="w-3 h-3" /> CONNECTED</>
                  ) : (
                    <><AlertCircle className="w-3 h-3" /> OFFLINE</>
                  )}
                </span>
              </div>
              <h3 className="font-semibold text-sm text-slate-200">PostgreSQL / pgvector</h3>
              <p className="text-xs text-slate-400 mt-1">Database connection status</p>
              <div className="mt-4 pt-3 border-t border-slate-800/80 flex justify-between text-xs">
                <span className="text-slate-500">Host</span>
                <span className="font-mono text-slate-300">localhost:5432</span>
              </div>
            </div>

            {/* LLM Provider Card */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all">
              <div className="flex justify-between items-start mb-4">
                <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
                  <Cpu className="w-5 h-5" />
                </div>
                <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-mono">
                  {health.llm_provider}
                </span>
              </div>
              <h3 className="font-semibold text-sm text-slate-200">LLM Provider</h3>
              <p className="text-xs text-slate-400 mt-1">Active AI model runtime</p>
              <div className="mt-4 pt-3 border-t border-slate-800/80 flex justify-between text-xs">
                <span className="text-slate-500">Provider</span>
                <span className="font-mono text-slate-300">{health.llm_provider}</span>
              </div>
            </div>
          </div>
        ) : null}
      </main>

      <footer className="max-w-4xl mx-auto w-full text-center text-xs text-slate-600 border-t border-slate-900 py-4">
        The Lenny Growth Assistant &copy; 2026 &bull; Ready for Phase 2: Database Schema & Migrations
      </footer>
    </div>
  )
}
