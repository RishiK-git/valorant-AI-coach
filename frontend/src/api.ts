import type { StatusResponse } from './types'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export async function submitVideo(file: File): Promise<string> {
  const form = new FormData()
  form.append('file', file)

  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    body: form,
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Upload failed (${res.status}): ${text}`)
  }

  const data = await res.json()
  return data.job_id as string
}

export async function pollStatus(jobId: string): Promise<StatusResponse> {
  const res = await fetch(`${API_BASE}/status/${jobId}`)

  if (!res.ok) {
    throw new Error(`Status check failed (${res.status})`)
  }

  return res.json()
}
