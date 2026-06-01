import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "股票分析",
  description: "股票市场分析与可视化工具",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" className={`${inter.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-zinc-50">
        <header className="border-b border-zinc-200 bg-white">
          <div className="max-w-7xl mx-auto px-3 md:px-4 py-2 md:py-3">
            <h1 className="text-lg md:text-xl font-bold text-zinc-900">股票分析</h1>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}