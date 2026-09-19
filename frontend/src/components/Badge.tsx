import type { ReactNode } from 'react'

export function Badge({ children, tone = 'slate' }: { children: ReactNode; tone?: 'green' | 'amber' | 'red' | 'blue' | 'slate' }) {
  const styles = {
    green: 'bg-emerald-50 text-emerald-700 ring-emerald-600/15',
    amber: 'bg-amber-50 text-amber-700 ring-amber-600/15',
    red: 'bg-rose-50 text-rose-700 ring-rose-600/15',
    blue: 'bg-sky-50 text-sky-700 ring-sky-600/15',
    slate: 'bg-slate-100 text-slate-700 ring-slate-500/15',
  }
  return <span className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ring-inset ${styles[tone]}`}>{children}</span>
}
