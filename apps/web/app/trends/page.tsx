import { TrendLine } from "@/components/charts";

export default function MonthlyTrends() {
  return <main className="mx-auto max-w-6xl px-6 py-12"><div className="glass rounded-3xl p-8"><h1 className="text-4xl font-black">Monthly Trends</h1><p className="mt-3 text-slate-300">Track month-over-month spend, category drift, and budget risk before it surprises you.</p><div className="mt-8"><TrendLine /></div></div></main>;
}
