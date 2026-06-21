"use client";

import { useState } from "react";
import { askAssistant } from "@/lib/api";

export default function ChatAssistant() {
  const [message, setMessage] = useState("How can I save more this month?");
  const [answer, setAnswer] = useState("Ask a question grounded in your uploaded statement data.");
  const [loading, setLoading] = useState(false);
  async function submit() {
    setLoading(true);
    try { const response = await askAssistant(message); setAnswer(response.answer); } catch { setAnswer("Start the FastAPI backend and run an audit first, then ask again."); } finally { setLoading(false); }
  }
  return <main className="mx-auto max-w-4xl px-6 py-12"><div className="glass rounded-[2rem] p-8"><p className="text-mint">AI Chat Assistant</p><h1 className="mt-2 text-4xl font-black">Ask grounded questions about your finances.</h1><textarea value={message} onChange={(event) => setMessage(event.target.value)} className="mt-6 min-h-32 w-full rounded-2xl border border-white/10 bg-black/30 p-4 text-white outline-none focus:border-mint" /><button onClick={submit} className="mt-4 rounded-full bg-mint px-6 py-3 font-bold text-ink">{loading ? "Thinking..." : "Ask FinPilot"}</button><div className="mt-6 rounded-3xl bg-white/5 p-6 text-slate-200">{answer}</div></div></main>;
}
