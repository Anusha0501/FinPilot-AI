import { getTransactions } from "@/lib/api";

export default async function SpendingAnalysis() {
  let rows: Array<Record<string, unknown>> = [];
  try { rows = await getTransactions(); } catch {}
  return <main className="mx-auto max-w-7xl px-6 py-12"><h1 className="text-4xl font-black">Spending Analysis</h1><div className="glass mt-6 overflow-hidden rounded-3xl"><table className="w-full text-left text-sm"><thead className="bg-white/5 text-slate-300"><tr><th className="p-4">Date</th><th>Merchant</th><th>Description</th><th>Amount</th></tr></thead><tbody>{rows.map((row) => <tr key={String(row.id)} className="border-t border-white/10"><td className="p-4">{String(row.posted_date)}</td><td>{String(row.merchant_name)}</td><td>{String(row.description_normalized)}</td><td>${String(row.amount)}</td></tr>)}</tbody></table></div></main>;
}
