import { useRef, useState } from 'react'
import { ArrowRight, FileText, Sparkles, UploadCloud, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { analyzeResume, fetchDemo } from '../lib/api'

export function HomePage() {
  const [file, setFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [dragActive, setDragActive] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()

  const selectFile = (candidate: File | undefined) => {
    setError('')
    if (!candidate) return
    if (candidate.type !== 'application/pdf' && !candidate.name.toLowerCase().endsWith('.pdf')) {
      setError('Please upload a PDF resume.')
      return
    }
    if (candidate.size > 5 * 1024 * 1024) {
      setError('The PDF must be 5 MB or smaller.')
      return
    }
    setFile(candidate)
  }

  const submit = async () => {
    if (!file) return setError('Upload a resume PDF first.')
    if (!jobDescription.trim()) return setError('Paste the job description first.')
    setLoading(true)
    setError('')
    try {
      const result = await analyzeResume(file, jobDescription)
      navigate('/results', { state: result })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed.')
    } finally {
      setLoading(false)
    }
  }

  const demo = async () => {
    setLoading(true)
    setError('')
    try {
      const result = await fetchDemo()
      navigate('/results', { state: result })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Demo is unavailable.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div className="overflow-hidden rounded-3xl bg-slate-900 px-6 py-12 text-white shadow-xl shadow-slate-300/20 sm:px-10 lg:px-12 lg:py-16">
        <div className="relative max-w-3xl">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-3 py-1.5 text-xs font-semibold text-slate-200"><Sparkles size={13} /> Evidence-first matching</div>
          <h1 className="max-w-2xl text-4xl font-black tracking-tight sm:text-5xl">AI Resume–Job Matcher</h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">See how well your resume aligns with the job you want—then understand exactly what is matched, missing, and worth improving.</p>
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-[0.9fr_1.1fr]">
        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between"><div><h2 className="font-bold">Upload Resume</h2><p className="mt-1 text-xs text-slate-500">PDF only · max 5 MB</p></div><FileText className="text-slate-400" size={20} /></div>
          {!file ? (
            <button type="button" onClick={() => inputRef.current?.click()} onDragEnter={(e) => { e.preventDefault(); setDragActive(true) }} onDragOver={(e) => e.preventDefault()} onDragLeave={() => setDragActive(false)} onDrop={(e) => { e.preventDefault(); setDragActive(false); selectFile(e.dataTransfer.files?.[0]) }} className={`flex min-h-64 w-full flex-col items-center justify-center rounded-2xl border-2 border-dashed p-6 text-center transition ${dragActive ? 'border-sky-400 bg-sky-50' : 'border-slate-200 bg-slate-50 hover:border-slate-300 hover:bg-white'}`}>
              <span className="mb-4 grid h-12 w-12 place-items-center rounded-2xl bg-white text-sky-600 shadow-sm"><UploadCloud size={22} /></span>
              <span className="text-sm font-bold text-slate-900">Drag & drop your resume</span>
              <span className="mt-1 text-sm text-slate-500">or click to browse a PDF</span>
            </button>
          ) : (
            <div className="flex min-h-64 items-center justify-center rounded-2xl border border-slate-200 bg-slate-50 p-6">
              <div className="w-full rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"><div className="flex items-center gap-3"><div className="grid h-11 w-11 place-items-center rounded-xl bg-rose-50 text-rose-600"><FileText size={20} /></div><div className="min-w-0 flex-1"><p className="truncate text-sm font-bold">{file.name}</p><p className="text-xs text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p></div><button onClick={() => setFile(null)} className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700"><X size={18} /></button></div></div>
            </div>
          )}
          <input ref={inputRef} type="file" accept="application/pdf,.pdf" className="hidden" onChange={(e) => selectFile(e.target.files?.[0])} />
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between"><div><h2 className="font-bold">Job Description</h2><p className="mt-1 text-xs text-slate-500">Paste the complete description for better evidence mapping.</p></div><span className="text-xs font-semibold text-slate-400">{jobDescription.length.toLocaleString()} / 30,000</span></div>
          <textarea value={jobDescription} onChange={(e) => setJobDescription(e.target.value.slice(0, 30000))} placeholder="Paste the job description here..." className="min-h-64 w-full resize-y rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm leading-6 outline-none transition placeholder:text-slate-400 focus:border-sky-400 focus:bg-white focus:ring-4 focus:ring-sky-500/10" />
          <div className="mt-4 rounded-xl bg-slate-50 px-4 py-3 text-xs leading-5 text-slate-500">Your results are based on evidence extracted from your resume and job description.</div>
        </section>
      </div>

      {error && <div className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700">{error}</div>}

      <div className="flex flex-col items-stretch justify-between gap-3 sm:flex-row sm:items-center">
        <button type="button" onClick={demo} disabled={loading} className="order-2 flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700 shadow-sm transition hover:border-slate-300 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60 sm:order-1">{loading ? 'Working...' : 'Try demo analysis'}</button>
        <button type="button" onClick={submit} disabled={loading} className="order-1 flex items-center justify-center gap-2 rounded-xl bg-slate-900 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60 sm:order-2">{loading ? 'Analyzing...' : 'Analyze Match'} <ArrowRight size={17} /></button>
      </div>
    </div>
  )
}
