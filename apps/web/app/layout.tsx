import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";
import { Nav } from "@/components/nav";

export const metadata: Metadata = { title: "FinPilot-AI", description: "AI personal finance audit agent" };

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return <html lang="en"><body><div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(102,227,180,0.16),_transparent_35%),radial-gradient(circle_at_top_right,_rgba(139,92,246,0.16),_transparent_30%)]"><Nav />{children}</div></body></html>;
}
