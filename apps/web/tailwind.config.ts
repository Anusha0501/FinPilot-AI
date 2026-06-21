import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0b1020",
        mint: "#66e3b4",
        violet: "#8b5cf6"
      },
      boxShadow: { glow: "0 24px 80px rgba(102, 227, 180, 0.18)" }
    }
  },
  plugins: []
};
export default config;
