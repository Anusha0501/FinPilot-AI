import { UploadPanel } from "@/components/upload-panel";

export default function UploadCenter() {
  return <main className="mx-auto max-w-5xl px-6 py-12"><div className="glass rounded-[2rem] p-10"><p className="text-mint">Upload Center</p><h1 className="mt-2 text-4xl font-black">Drop a PDF statement, then process and audit it.</h1><p className="mt-4 text-slate-300">The demo upload flow stores the file, extracts transactions, runs categorization, detects subscriptions, and refreshes analytics for the dashboard.</p><UploadPanel /></div></main>;
}
