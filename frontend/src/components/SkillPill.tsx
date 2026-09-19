import { Check, Minus, X } from 'lucide-react'
import type { SkillItem } from '../types'

export function SkillPill({ item }: { item: SkillItem }) {
  const matched = item.status === 'matched'
  const partial = item.status === 'partial'
  return (
    <div className={`group rounded-xl border p-3 ${matched ? 'border-emerald-200 bg-emerald-50/60' : partial ? 'border-amber-200 bg-amber-50/60' : 'border-rose-200 bg-rose-50/60'}`}>
      <div className="flex items-center justify-between gap-3">
        <div className="flex min-w-0 items-center gap-2">
          <span className={`grid h-7 w-7 shrink-0 place-items-center rounded-lg ${matched ? 'bg-emerald-100 text-emerald-700' : partial ? 'bg-amber-100 text-amber-700' : 'bg-rose-100 text-rose-700'}`}>
            {matched ? <Check size={14} /> : partial ? <Minus size={14} /> : <X size={14} />}
          </span>
          <span className="truncate text-sm font-bold text-slate-900">{item.skill}</span>
        </div>
      </div>
      {item.evidence && <p className="mt-2 text-xs leading-5 text-slate-600"><span className="font-semibold text-slate-700">Evidence:</span> “{item.evidence}”</p>}
      {!item.evidence && item.status === 'missing' && <p className="mt-2 text-xs text-slate-500">No supporting resume evidence found.</p>}
    </div>
  )
}
