const ideas = ["Cancel one unused subscription", "Cap food delivery to 2x/week", "Move recurring bills to a dedicated account", "Review shopping merchants over $100"];
export default function SavingsPlanner() {
  return <main className="mx-auto max-w-6xl px-6 py-12"><h1 className="text-4xl font-black">Savings Planner</h1><div className="mt-6 grid gap-4 md:grid-cols-2">{ideas.map((idea, index) => <article key={idea} className="glass rounded-3xl p-6"><p className="text-mint">Step {index + 1}</p><h2 className="mt-2 text-2xl font-bold">{idea}</h2><p className="mt-2 text-slate-300">FinPilot converts audit findings into practical experiments with estimated savings impact.</p></article>)}</div></main>;
}
