import { useState, useRef } from 'react'
import { Upload } from 'lucide-react'

const ACCEPTED = '.mp4,.mov,.avi,.mkv,.webm,.flv,.wmv,.m4v,.ts,.mts'

interface Props {
  onSubmit: (file: File) => void
  disabled: boolean
}

export default function UploadForm({ onSubmit, disabled }: Props) {
  const [selected, setSelected] = useState<File | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  function handleFile(file: File) {
    setSelected(file)
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (selected) onSubmit(selected)
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col items-center gap-6">
      <div
        onClick={() => inputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        className="w-full max-w-lg border-2 border-dashed border-zinc-600 rounded-xl p-12 flex flex-col items-center gap-3 cursor-pointer hover:border-zinc-400 transition-colors"
      >
        <Upload className="text-zinc-500" size={32} />
        {selected ? (
          <span className="text-zinc-200 font-medium">{selected.name}</span>
        ) : (
          <>
            <span className="text-zinc-300 font-medium">Drop a video or click to browse</span>
            <span className="text-zinc-500 text-sm">MP4, MOV, AVI, MKV, WebM and more</span>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED}
          className="hidden"
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        />
      </div>

      <button
        type="submit"
        disabled={!selected || disabled}
        className="px-8 py-3 bg-red-600 hover:bg-red-500 disabled:bg-zinc-700 disabled:text-zinc-500 text-white font-semibold rounded-lg transition-colors cursor-pointer disabled:cursor-not-allowed"
      >
        Analyze
      </button>
    </form>
  )
}
