export interface TimelineEvent {
  timestamp: string
  title: string
  observation: string
}

export interface KeyMoment {
  timestamp: string
  title: string
  why: string
}

export interface Coaching {
  mistake: string
  why: string
  fix: string
  positive: string
}

export interface CoachingReport {
  summary: string
  timeline: TimelineEvent[]
  key_moment: KeyMoment
  coaching: Coaching
  confidence: number
}

export type JobStatus = 'pending' | 'running' | 'completed' | 'failed'

export interface StatusResponse {
  job_id: string
  status: JobStatus
  result: CoachingReport | null
  error: string | null
}
