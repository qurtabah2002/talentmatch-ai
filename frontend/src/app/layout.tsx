import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TalentMatch AI — Resume Screener",
  description:
    "AI-powered resume screening system with human oversight and fairness monitoring. Compliant with EU AI Act, NIST AI RMF, and SOC 2.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">
        <nav className="border-b border-[#2a2a3a] bg-[#111118]">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
            <a href="/" className="flex items-center gap-2 text-lg font-bold">
              <span className="text-2xl">🎯</span>
              <span>TalentMatch AI</span>
            </a>
            <div className="flex gap-6 text-sm">
              <a href="/" className="text-[#8888a0] hover:text-white transition">
                Screen
              </a>
              <a href="/dashboard" className="text-[#8888a0] hover:text-white transition">
                Fairness Dashboard
              </a>
              <a href="/model" className="text-[#8888a0] hover:text-white transition">
                Model Info
              </a>
            </div>
          </div>
        </nav>
        <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
