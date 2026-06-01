"use client";

import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import StockChart from "@/components/StockChart";
import FinancialPanel from "@/components/FinancialPanel";

const POPULAR_STOCKS = [
  { symbol: "AAPL", name: "Apple" },
  { symbol: "MSFT", name: "Microsoft" },
  { symbol: "GOOGL", name: "Alphabet" },
  { symbol: "AMZN", name: "Amazon" },
  { symbol: "TSLA", name: "Tesla" },
  { symbol: "META", name: "Meta" },
  { symbol: "NVDA", name: "NVIDIA" },
];

export default function Home() {
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
  const [selectedName, setSelectedName] = useState<string>("");

  function handleSelect(symbol: string, name: string) {
    setSelectedSymbol(symbol);
    setSelectedName(name);
  }

  return (
    <div className="min-h-screen bg-zinc-50">
      {/* 顶部区域 */}
      <div className="bg-white border-b border-zinc-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold text-zinc-900 mb-6">📊 股票分析</h1>
          
          {/* 热门股票 */}
          <div className="mb-6">
            <p className="text-lg font-semibold text-zinc-800 mb-3">热门股票</p>
            <div className="grid grid-cols-2 gap-3">
              {POPULAR_STOCKS.map((stock) => (
                <button
                  key={stock.symbol}
                  onClick={() => handleSelect(stock.symbol, stock.name)}
                  className="w-full p-4 bg-blue-600 text-white rounded-xl text-center cursor-pointer"
                  style={{ touchAction: 'manipulation' }}
                >
                  <div className="text-xl font-bold">{stock.symbol}</div>
                  <div className="text-sm opacity-90">{stock.name}</div>
                </button>
              ))}
            </div>
          </div>

          {/* 搜索框 */}
          <div className="mb-4">
            <p className="text-lg font-semibold text-zinc-800 mb-3">搜索其他股票</p>
            <SearchBar onSelect={handleSelect} />
          </div>
        </div>
      </div>

      {/* 内容区域 */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {!selectedSymbol ? (
          <div className="bg-white rounded-xl border border-zinc-200 p-8 text-center">
            <div className="text-6xl mb-4">👆</div>
            <h3 className="text-xl font-bold text-zinc-900 mb-2">点击上面的股票按钮开始</h3>
            <p className="text-zinc-500">选择一个热门股票或搜索其他股票</p>
          </div>
        ) : (
          <>
            <div className="mb-4 flex items-center justify-between">
              <div>
                <span className="text-xl font-bold text-zinc-900">{selectedSymbol}</span>
                <span className="ml-2 text-zinc-500">{selectedName}</span>
              </div>
              <button
                onClick={() => {
                  setSelectedSymbol(null);
                  setSelectedName("");
                }}
                className="text-zinc-500 underline"
              >
                返回
              </button>
            </div>
            <div className="flex flex-col gap-4">
              <StockChart symbol={selectedSymbol} />
              <FinancialPanel symbol={selectedSymbol} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}
