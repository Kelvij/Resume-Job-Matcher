import type { ReactNode } from 'react'

export function SectionCard({ title, eyebrow, children, action }: { title: string; eyebrow?: string; children: ReactNode; action?: ReactNode }) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white shadow-sm shadow-slate-200/40">
      <div className="flex items-start justify-between gap-4 border-b border-slate-100 px-5 py-4">
        <div>
          {eyebrow && <p className="mb-1 text-[11px] font-bold uppercase tracking-[0.16em] text-slate-400">{eyebrow}</p>}
          <h2 className="text-lg font-bold text-slate-900">{title}</h2>
        </div>
        {action}
      </div>
      <div className="p-5">{children}</div>
    </section>
  )
}
