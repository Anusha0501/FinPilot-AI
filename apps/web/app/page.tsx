import { CategoryPie, TrendLine } from "@/components/charts";
import { getSummary } from "@/lib/api";

function money(value: string) { return `$${Number(value).toLocaleString()}`; }

export default async function Dashboard() {
  let summary = null;
  try { summary = await getSummary(); } catch { summary = { total_income: "0", total_expenses: "0", net_savings: "0", savings_rate: 0, transaction_count: 0, top_merchants: [], category_breakdown: [], insights: [] }; }
  return <main className="mx-auto max-w-7xl px-6 pb-16">
    <section className="py-10"><p className="mb-3 text-sm font-semibold uppercase tracking-[0.3em] text-mint">Personal Finance Audit Agent</p><h1 className="max-w-4xl text-5xl font-black tracking-tight md:text-7xl">Turn bank statements into boardroom-grade money intelligence.</h1><p className="mt-5 max-w-2xl text-lg text-slate-300">Upload PDFs, extract transactions, classify spend, detect forgotten subscriptions, and ask grounded questions about your money.</p></section>
    <section className="grid gap-4 md:grid-cols-4">{[["Income", money(summary.total_income)], ["Expenses", money(summary.total_expenses)], ["Net Savings", money(summary.net_savings)], ["Transactions", summary.transaction_count]].map(([label, value]) => <div key={label} className="glass rounded-3xl p-5 shadow-glow"><p className="text-sm text-slate-400">{label}</p><p className="mt-2 text-3xl font-bold">{value}</p></div>)}</section>
    <section className="mt-6 grid gap-6 lg:grid-cols-2"><div className="glass rounded-3xl p-6"><h2 className="text-xl font-bold">Category Breakdown</h2><CategoryPie data={summary.category_breakdown} /></div><div className="glass rounded-3xl p-6"><h2 className="text-xl font-bold">Spending Trend</h2><TrendLine /></div></section>
    <section className="mt-6 grid gap-4 md:grid-cols-2">{summary.insights.map((insight) => <article key={insight.title} className="glass rounded-3xl p-6"><p className="text-mint">Potential impact: {money(insight.estimated_impact)}</p><h3 className="mt-2 text-2xl font-bold">{insight.title}</h3><p className="mt-2 text-slate-300">{insight.body}</p></article>)}</section>
  </main>;
}
