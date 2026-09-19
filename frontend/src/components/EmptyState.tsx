import type { ReactNode } from 'react'

export function EmptyState({ title, message, icon }: { title: string; message: string; icon: ReactNode }) {
  return (
    <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
      <div className="mx-auto mb-4 grid h-12 w-12 place-items-center rounded-2xl bg-slate-100 text-slate-500">{icon}</div>
      <h3 className="text-base font-bold text-slate-900">{title}</h3>
      <p className="mx-auto mt-1 max-w-md text-sm leading-6 text-slate-500">{message}</p>
    </div>
  )
}
