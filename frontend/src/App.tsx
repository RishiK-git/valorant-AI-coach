import { useState, useEffect, useRef } from 'react'
import { submitVideo, pollStatus } from './api'
import type { CoachingReport as CoachingReportType, JobStatus } from './types'
import UploadForm from './components/UploadForm'
import AnalysisProgress from './components/AnalysisProgress'
import CoachingReport from './components/CoachingReport'
import { AlertCircle, RotateCcw } from 'lucide-react'
import './index.css'

type AppState =
  | { stage: 'idle' }
  | { stage: 'uploading' }
  | { stage: 'polling'; jobId: string; status: JobStatus }
  | { stage: 'done'; report: CoachingReportType }
  | { stage: 'error'; message: string }

const POLL_INTERVAL_MS = 2000

export default function App() {
  const [state, setState] = useState<AppState>({ stage: 'idle' })
  const pollTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    return () => {
      if (pollTimer.current) clearTimeout(pollTimer.current)
    }
  }, [])

  async function handleUpload(file: File) {
    setState({ stage: 'uploading' })
    try {
      const jobId = await submitVideo(file)
      setState({ stage: 'polling', jobId, status: 'pending' })
      schedulePoll(jobId)
    } catch (err) {
      setState({ stage: 'error', message: String(err) })
    }
  }

  function schedulePoll(jobId: string) {
    pollTimer.current = setTimeout(() => poll(jobId), POLL_INTERVAL_MS)
  }

  async function poll(jobId: string) {
    try {
      const data = await pollStatus(jobId)
      if (data.status === 'completed' && data.result) {
        setState({ stage: 'done', report: data.result })
      } else if (data.status === 'failed') {
        setState({ stage: 'error', message: data.error ?? 'Analysis failed.' })
      } else {
        setState({ stage: 'polling', jobId, status: data.status })
        schedulePoll(jobId)
      }
    } catch (err) {
      setState({ stage: 'error', message: String(err) })
    }
  }

  function reset() {
    if (pollTimer.current) clearTimeout(pollTimer.current)
    setState({ stage: 'idle' })
  }

  return (
    <div className="min-h-screen bg-zinc-900 text-zinc-100 flex flex-col">
      <header className="border-b border-zinc-800 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold tracking-tight">Valorant AI Coach</h1>
          <p className="text-zinc-500 text-sm">Upload a clip. Get coaching.</p>
        </div>
        {state.stage !== 'idle' && (
          <button
            onClick={reset}
            className="flex items-center gap-2 text-zinc-400 hover:text-zinc-200 text-sm transition-colors cursor-pointer"
          >
            <RotateCcw size={14} />
            Start over
          </button>
        )}
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-6 py-12 gap-8">
        {state.stage === 'idle' && (
          <UploadForm onSubmit={handleUpload} disabled={false} />
        )}

        {state.stage === 'uploading' && (
          <p className="text-zinc-400">Uploading...</p>
        )}

        {state.stage === 'polling' && (
          <AnalysisProgress status={state.status} />
        )}

        {state.stage === 'done' && (
          <CoachingReport report={state.report} />
        )}

        {state.stage === 'error' && (
          <div className="flex flex-col items-center gap-4 text-center max-w-md">
            <AlertCircle size={32} className="text-red-500" />
            <p className="text-zinc-300">{state.message}</p>
            <button
              onClick={reset}
              className="px-6 py-2 bg-zinc-700 hover:bg-zinc-600 rounded-lg text-sm transition-colors cursor-pointer"
            >
              Try again
            </button>
          </div>
        )}
      </main>
    </div>
  )
}
