import { useEffect, useRef } from 'react'
import { X } from 'lucide-react'

interface Props {
  file: File
  seekTo: number | null
  onClose: () => void
}

function parseTimestamp(timestamp: string): number {
  const [minutes, seconds] = timestamp.split(':').map(Number)
  return minutes * 60 + seconds
}

export default function VideoPanel({ file, seekTo, onClose }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const blobUrlRef = useRef<string | null>(null)

  useEffect(() => {
    const url = URL.createObjectURL(file)
    blobUrlRef.current = url
    if (videoRef.current) videoRef.current.src = url
    return () => URL.revokeObjectURL(url)
  }, [file])

  useEffect(() => {
    if (seekTo === null || !videoRef.current) return
    const video = videoRef.current

    function seek() {
      video.currentTime = seekTo!
      video.pause()
    }

    if (video.readyState >= 1) {
      seek()
    } else {
      video.addEventListener('loadedmetadata', seek, { once: true })
    }
  }, [seekTo])

  return (
    <div className="flex flex-col gap-3 w-full">
      <div className="flex items-center justify-between">
        <span className="text-zinc-400 text-sm font-semibold uppercase tracking-wide">Clip Preview</span>
        <button
          onClick={onClose}
          className="text-zinc-500 hover:text-zinc-200 transition-colors cursor-pointer"
        >
          <X size={18} />
        </button>
      </div>
      <video
        ref={videoRef}
        controls
        className="w-full rounded-xl bg-black"
      />
    </div>
  )
}

export { parseTimestamp }
