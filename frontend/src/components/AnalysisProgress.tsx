import { Loader2, CheckCircle } from 'lucide-react'
import type { JobStatus } from '../types'

const STAGES: { status: JobStatus; label: string }[] = [
  { status: 'pending', label: 'Queued' },
  { status: 'running', label: 'Extracting frames & analyzing with Gemini' },
  { status: 'completed', label: 'Done' },
]

interface Props {
  status: JobStatus
}

export default function AnalysisProgress({ status }: Props) {
  const currentIndex = STAGES.findIndex((s) => s.status === status)

  return (
    <div className="flex flex-col items-center gap-6">
      <div className="flex flex-col gap-4 w-full max-w-sm">
        {STAGES.map((stage, i) => {
          const isPast = i < currentIndex
          const isCurrent = i === currentIndex
          const isFuture = i > currentIndex

          return (
            <div key={stage.status} className="flex items-center gap-3">
              {isCurrent ? (
                <Loader2 size={20} className="text-red-500 animate-spin shrink-0" />
              ) : isPast ? (
                <CheckCircle size={20} className="text-green-500 shrink-0" />
              ) : (
                <div className="w-5 h-5 rounded-full border-2 border-zinc-600 shrink-0" />
              )}
              <span
                className={
                  isCurrent
                    ? 'text-zinc-100 font-medium'
                    : isPast
                    ? 'text-zinc-400'
                    : isFuture
                    ? 'text-zinc-600'
                    : ''
                }
              >
                {stage.label}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
