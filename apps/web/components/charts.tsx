"use client";

import { Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const colors = ["#66e3b4", "#8b5cf6", "#38bdf8", "#f97316", "#f43f5e", "#eab308"];

export function CategoryPie({ data }: { data: Array<{ category: string; amount: string }> }) {
  const chartData = data.map((item) => ({ name: item.category, value: Number(item.amount) }));
  return <ResponsiveContainer width="100%" height={260}><PieChart><Pie data={chartData} dataKey="value" nameKey="name" innerRadius={62} outerRadius={96}>{chartData.map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer>;
}

export function TrendLine() {
  const data = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"].map((month, index) => ({ month, spend: 2200 + index * 140 + (index % 2) * 260 }));
  return <ResponsiveContainer width="100%" height={260}><LineChart data={data}><XAxis dataKey="month" stroke="#94a3b8" /><YAxis stroke="#94a3b8" /><Tooltip /><Line type="monotone" dataKey="spend" stroke="#66e3b4" strokeWidth={3} dot={false} /></LineChart></ResponsiveContainer>;
}
