import type { Analysis, HistoryItem } from '../types'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = 'Something went wrong.'
    try {
      const body = await response.json()
      message = body.detail || message
    } catch {
      // Keep generic message when the server does not return JSON.
    }
    throw new Error(message)
  }
  return response.json() as Promise<T>
}

export async function analyzeResume(file: File, jobDescription: string): Promise<Analysis> {
  const form = new FormData()
  form.append('resume', file)
  form.append('job_description', jobDescription)
  const response = await fetch(`${API_BASE}/analyze`, { method: 'POST', body: form })
  return parseResponse<Analysis>(response)
}

export async function fetchDemo(): Promise<Analysis> {
  const response = await fetch(`${API_BASE}/demo`)
  return parseResponse<Analysis>(response)
}

export async function fetchHistory(): Promise<HistoryItem[]> {
  const response = await fetch(`${API_BASE}/history`)
  return parseResponse<HistoryItem[]>(response)
}

export async function fetchHistoryItem(id: string): Promise<Analysis> {
  const response = await fetch(`${API_BASE}/history/${id}`)
  return parseResponse<Analysis>(response)
}

export async function deleteHistoryItem(id: string): Promise<void> {
  const response = await fetch(`${API_BASE}/history/${id}`, { method: 'DELETE' })
  if (!response.ok) {
    let message = 'Unable to delete this report.'
    try {
      const body = await response.json()
      message = body.detail || message
    } catch {
      // Ignore parsing failure.
    }
    throw new Error(message)
  }
}
