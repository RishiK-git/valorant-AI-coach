import { useState } from 'react'
import { AlertCircle, Star, Clock, Crosshair, Lightbulb, ThumbsUp } from 'lucide-react'
import type { CoachingReport as CoachingReportType } from '../types'
import VideoPanel, { parseTimestamp } from './VideoPanel'

interface Props {
  report: CoachingReportType
  file: File
}

export default function CoachingReport({ report, file }: Props) {
  const [seekTo, setSeekTo] = useState<number | null>(null)
  const [panelOpen, setPanelOpen] = useState(false)

  const confidencePct = Math.round(report.confidence * 100)
  const confidenceColor =
    report.confidence >= 0.75
      ? 'text-green-400'
      : report.confidence >= 0.5
      ? 'text-yellow-400'
      : 'text-red-400'

  function handleTimestampClick(timestamp: string) {
    setSeekTo(parseTimestamp(timestamp))
    setPanelOpen(true)
  }

  return (
    <div className={`flex gap-6 w-full max-w-6xl mx-auto items-start transition-all`}>

      {/* Report */}
      <div className={`flex flex-col gap-6 ${panelOpen ? 'w-1/2' : 'w-full max-w-2xl mx-auto'} transition-all`}>

        {/* Summary + confidence */}
        <div className="bg-zinc-800 rounded-xl p-5 flex items-start justify-between gap-4">
          <p className="text-zinc-100 text-lg leading-snug">{report.summary}</p>
          <span className={`text-sm font-semibold shrink-0 ${confidenceColor}`}>
            {confidencePct}% confidence
          </span>
        </div>

        {/* Key moment */}
        <div className="bg-zinc-800 border border-red-700/40 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <Star size={16} className="text-red-500" />
            <span className="text-red-400 text-sm font-semibold uppercase tracking-wide">Key Moment</span>
            <button
              onClick={() => handleTimestampClick(report.key_moment.timestamp)}
              className="ml-auto text-zinc-500 hover:text-red-400 text-sm flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Clock size={13} />{report.key_moment.timestamp}
            </button>
          </div>
          <p className="text-zinc-100 font-medium mb-1">{report.key_moment.title}</p>
          <p className="text-zinc-400 text-sm leading-relaxed">{report.key_moment.why}</p>
        </div>

        {/* Timeline */}
        <div className="bg-zinc-800 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <Clock size={16} className="text-zinc-400" />
            <span className="text-zinc-400 text-sm font-semibold uppercase tracking-wide">Timeline</span>
          </div>
          <div className="flex flex-col gap-4">
            {report.timeline.map((event, i) => (
              <div key={i} className="flex gap-4">
                <button
                  onClick={() => handleTimestampClick(event.timestamp)}
                  className="text-zinc-500 hover:text-red-400 text-sm font-mono shrink-0 mt-0.5 w-10 text-left transition-colors cursor-pointer"
                >
                  {event.timestamp}
                </button>
                <div>
                  <p className="text-zinc-200 font-medium text-sm">{event.title}</p>
                  <p className="text-zinc-400 text-sm leading-relaxed">{event.observation}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Coaching */}
        <div className="bg-zinc-800 rounded-xl p-5 flex flex-col gap-5">
          <div className="flex items-center gap-2">
            <Crosshair size={16} className="text-zinc-400" />
            <span className="text-zinc-400 text-sm font-semibold uppercase tracking-wide">Coaching</span>
          </div>

          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-2">
              <AlertCircle size={14} className="text-red-400 shrink-0" />
              <span className="text-red-400 text-xs font-semibold uppercase tracking-wide">Biggest Mistake</span>
            </div>
            <p className="text-zinc-100 font-medium">{report.coaching.mistake}</p>
            <p className="text-zinc-400 text-sm leading-relaxed mt-1">{report.coaching.why}</p>
          </div>

          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-2">
              <Lightbulb size={14} className="text-yellow-400 shrink-0" />
              <span className="text-yellow-400 text-xs font-semibold uppercase tracking-wide">Fix</span>
            </div>
            <p className="text-zinc-200 text-sm leading-relaxed">{report.coaching.fix}</p>
          </div>

          {report.coaching.positive && (
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <ThumbsUp size={14} className="text-green-400 shrink-0" />
                <span className="text-green-400 text-xs font-semibold uppercase tracking-wide">Positive</span>
              </div>
              <p className="text-zinc-200 text-sm leading-relaxed">{report.coaching.positive}</p>
            </div>
          )}
        </div>

      </div>

      {/* Video panel */}
      {panelOpen && (
        <div className="w-1/2 sticky top-6">
          <VideoPanel
            file={file}
            seekTo={seekTo}
            onClose={() => setPanelOpen(false)}
          />
        </div>
      )}

    </div>
  )
}
