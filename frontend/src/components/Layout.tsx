import { Link, NavLink, Outlet } from 'react-router-dom'
import { BrainCircuit, Clock3 } from 'lucide-react'

export function Layout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="sticky top-0 z-20 border-b border-slate-200/80 bg-white/90 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link to="/" className="flex items-center gap-2.5 font-extrabold tracking-tight">
            <span className="grid h-9 w-9 place-items-center rounded-xl bg-slate-900 text-white"><BrainCircuit size={18} /></span>
            <span>Resume<span className="text-sky-600">Match</span></span>
          </Link>
          <nav className="flex items-center gap-1 rounded-xl border border-slate-200 bg-slate-50 p-1">
            <NavLink to="/" end className={({ isActive }) => `rounded-lg px-3 py-1.5 text-sm font-semibold transition ${isActive ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}>Matcher</NavLink>
            <NavLink to="/history" className={({ isActive }) => `flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-semibold transition ${isActive ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}><Clock3 size={14} /> History</NavLink>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <Outlet />
      </main>
    </div>
  )
}
