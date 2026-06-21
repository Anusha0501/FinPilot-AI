import { getSubscriptions } from "@/lib/api";

export default async function SubscriptionTracker() {
  let rows: Array<Record<string, unknown>> = [];
  try { rows = await getSubscriptions(); } catch {}
  return <main className="mx-auto max-w-6xl px-6 py-12"><h1 className="text-4xl font-black">Subscription Tracker</h1><div className="mt-6 grid gap-4 md:grid-cols-3">{rows.map((item) => <article key={String(item.id)} className="glass rounded-3xl p-6"><p className="text-sm uppercase tracking-widest text-mint">{String(item.status)}</p><h2 className="mt-2 text-2xl font-bold">{String(item.merchant_name)}</h2><p className="mt-3 text-slate-300">Typical charge: ${String(item.typical_amount)}</p><p className="text-slate-400">Cadence: {String(item.cadence)}</p></article>)}</div></main>;
}
