import { useEffect, useState } from 'react'
import { ArrowRight, CalendarDays, FileText, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { deleteHistoryItem, fetchHistory, fetchHistoryItem } from '../lib/api'
import type { HistoryItem } from '../types'
import { Badge } from '../components/Badge'
import { EmptyState } from '../components/EmptyState'

export function HistoryPage() {
  const [items, setItems] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const refresh = async () => {
    setLoading(true)
    setError('')
    try { setItems(await fetchHistory()) } catch (err) { setError(err instanceof Error ? err.message : 'Unable to load history.') } finally { setLoading(false) }
  }

  useEffect(() => { refresh() }, [])

  const open = async (id: string) => {
    try { const report = await fetchHistoryItem(id); navigate('/results', { state: report }) } catch (err) { setError(err instanceof Error ? err.message : 'Unable to open report.') }
  }

  const remove = async (id: string) => {
    try { await deleteHistoryItem(id); setItems((current) => current.filter((item) => item.id !== id)) } catch (err) { setError(err instanceof Error ? err.message : 'Unable to delete report.') }
  }

  return <div className="space-y-6"><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-slate-400">Saved analyses</p><h1 className="mt-1 text-3xl font-black tracking-tight">History</h1><p className="mt-2 text-sm text-slate-500">Only report metadata and structured analysis are stored—uploaded PDFs are not retained.</p></div>{error && <div className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700">{error}</div>}{loading ? <div className="grid gap-3">{Array.from({ length: 4 }).map((_, i) => <div key={i} className="h-24 animate-pulse rounded-2xl bg-slate-200" />)}</div> : items.length ? <div className="space-y-3">{items.map((item) => <div key={item.id} className="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:flex-row sm:items-center"><div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-slate-100 text-slate-600"><FileText size={19} /></div><div className="min-w-0 flex-1"><p className="truncate font-bold">{item.resume_name}</p><p className="mt-1 text-sm text-slate-500">{item.job_title || 'Job title not detected'}{item.company_name ? ` · ${item.company_name}` : ''}</p><p className="mt-2 flex items-center gap-1.5 text-xs font-semibold text-slate-400"><CalendarDays size={13} /> {new Date(item.created_at).toLocaleString()}</p></div><div className="flex items-center gap-2"><Badge tone={item.score >= 75 ? 'green' : item.score >= 55 ? 'amber' : 'red'}>{item.score}/100</Badge><button onClick={() => open(item.id)} className="rounded-lg border border-slate-200 p-2 text-slate-600 hover:bg-slate-50" title="Open report"><ArrowRight size={16} /></button><button onClick={() => remove(item.id)} className="rounded-lg border border-slate-200 p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600" title="Delete report"><Trash2 size={16} /></button></div></div>)}</div> : <EmptyState title="No saved analyses yet" message="Run your first real analysis and it will appear here. Demo runs are intentionally not stored." icon={<FileText size={20} />} />}</div>
}
