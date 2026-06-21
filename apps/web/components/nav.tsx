import Link from "next/link";

const links = [
  ["Dashboard", "/"], ["Upload", "/upload"], ["Analysis", "/analysis"],
  ["Subscriptions", "/subscriptions"], ["Trends", "/trends"], ["Planner", "/planner"], ["AI Chat", "/chat"]
];

export function Nav() {
  return <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
    <Link href="/" className="text-xl font-black tracking-tight">FinPilot<span className="text-mint">.AI</span></Link>
    <div className="hidden gap-2 md:flex">
      {links.map(([label, href]) => <Link key={href} href={href} className="rounded-full px-3 py-2 text-sm text-slate-300 hover:bg-white/10 hover:text-white">{label}</Link>)}
    </div>
  </nav>;
}
