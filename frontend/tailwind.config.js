/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#6366f1", dark: "#4f46e5" },
        danger: { DEFAULT: "#ef4444", dark: "#dc2626" },
        warning: { DEFAULT: "#f59e0b", dark: "#d97706" },
        success: { DEFAULT: "#10b981", dark: "#059669" },
      },
    },
  },
  plugins: [],
};
