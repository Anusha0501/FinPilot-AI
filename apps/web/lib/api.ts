export type Summary = {
  total_income: string;
  total_expenses: string;
  net_savings: string;
  savings_rate: number;
  transaction_count: number;
  top_merchants: Array<{ merchant: string; amount: string }>;
  category_breakdown: Array<{ category: string; amount: string }>;
  insights: Array<{ title: string; body: string; estimated_impact: string }>;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { ...init, cache: "no-store" });
  if (!response.ok) throw new Error(`FinPilot API error: ${response.status}`);
  return response.json() as Promise<T>;
}

export function getSummary() {
  return request<Summary>("/analytics/summary");
}

export function getTransactions() {
  return request<Array<Record<string, unknown>>>("/transactions");
}

export function getSubscriptions() {
  return request<Array<Record<string, unknown>>>("/subscriptions");
}

export async function askAssistant(message: string) {
  return request<{ answer: string; evidence: unknown[]; disclaimer: string }>("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });
}
