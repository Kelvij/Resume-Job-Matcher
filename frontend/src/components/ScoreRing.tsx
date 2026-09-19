export function ScoreRing({ score }: { score: number }) {
  const radius = 62
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference
  const tone = score >= 75 ? 'text-emerald-500' : score >= 55 ? 'text-amber-500' : 'text-rose-500'
  return (
    <div className="relative h-44 w-44 shrink-0">
      <svg viewBox="0 0 150 150" className="h-full w-full -rotate-90">
        <circle cx="75" cy="75" r={radius} fill="none" stroke="currentColor" strokeWidth="10" className="text-slate-100" />
        <circle cx="75" cy="75" r={radius} fill="none" stroke="currentColor" strokeWidth="10" strokeLinecap="round" className={tone} strokeDasharray={circumference} strokeDashoffset={offset} />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-4xl font-black tracking-tight text-slate-900">{score}</span>
        <span className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">out of 100</span>
      </div>
    </div>
  )
}
