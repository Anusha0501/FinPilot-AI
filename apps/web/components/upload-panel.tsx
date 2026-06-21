"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export function UploadPanel() {
  const [status, setStatus] = useState("Choose a PDF bank statement to begin.");
  const [busy, setBusy] = useState(false);

  async function upload(file: File) {
    setBusy(true);
    setStatus("Uploading statement...");
    try {
      const form = new FormData();
      form.append("file", file);
      const uploaded = await fetch(`${API_BASE}/statements`, { method: "POST", body: form });
      if (!uploaded.ok) throw new Error("Upload failed");
      const payload = await uploaded.json();
      setStatus("Extracting transactions...");
      await fetch(`${API_BASE}/statements/${payload.statement_id}/process`, { method: "POST" });
      setStatus("Running finance audit agent...");
      await fetch(`${API_BASE}/agents/audit`, { method: "POST" });
      setStatus("Audit complete. Open the dashboard to review insights.");
    } catch {
      setStatus("Upload failed. Confirm the backend is running and the file is a text-based PDF.");
    } finally {
      setBusy(false);
    }
  }

  return <div className="mt-8 rounded-3xl border border-dashed border-mint/50 p-12 text-center text-slate-300">
    <input type="file" accept="application/pdf" disabled={busy} onChange={(event) => event.target.files?.[0] && upload(event.target.files[0])} className="mx-auto block rounded-2xl bg-white/10 p-4" />
    <p className="mt-4">{status}</p>
  </div>;
}
