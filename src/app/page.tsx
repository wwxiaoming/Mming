"use client";

import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import StockChart from "@/components/StockChart";
import FinancialPanel from "@/components/FinancialPanel";

const POPULAR_STOCKS = [
  { symbol: "AAPL", name: "Apple Inc." },
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
    <div className="flex flex-1 flex-col">
      <div className="border-b border-zinc-200 bg-white">
        <div className="max-w-7xl mx-auto px-3 md:px-4 py-6">
          <div className="text-center mb-6">
            <h2 className="text-xl md:text-2xl font-bold text-zinc-900 mb-2">
              🔍 搜索您感兴趣的股票
            </h2>
            <p className="text-sm text-zinc-500">
              输入股票代码或公司名称进行搜索
            </p>
          </div>
          <SearchBar onSelect={handleSelect} />
          
          {/* 热门股票快捷选择 */}
          <div className="mt-8">
            <p className="text-base font-bold text-zinc-800 mb-4">热门股票（点一下就看）：</p>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {POPULAR_STOCKS.map((stock) => (
                <button
                  key={stock.symbol}
                  onClick={() => handleSelect(stock.symbol, stock.name)}
                  className="px-4 py-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl font-semibold text-lg hover:from-blue-600 hover:to-blue-700 active:scale-95 transition-all shadow-md"
                >
                  <div>{stock.symbol}</div>
                  <div className="text-xs opacity-90 mt-1">{stock.name}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
      
      {selectedSymbol && selectedName && (
        <div className="max-w-7xl mx-auto w-full px-3 md:px-4 pt-4">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-bold text-zinc-900">
              {selectedSymbol}
              <span className="ml-2 text-sm font-normal text-zinc-500">
                {selectedName}
              </span>
            </h2>
            <button
              onClick={() => {
                setSelectedSymbol(null);
                setSelectedName("");
              }}
              className="text-sm text-zinc-500 hover:text-zinc-700"
            >
              清除选择
            </button>
          </div>
        </div>
      )}
      
      <div className="flex flex-1 max-w-7xl mx-auto w-full flex-col md:flex-row gap-4 md:gap-6 px-3 md:px-4 py-4 md:py-6">
        {!selectedSymbol ? (
          <div className="flex-1 flex items-center justify-center min-h-[400px] text-center">
            <div className="bg-white rounded-xl border border-zinc-200 p-8 max-w-md">
              <div className="text-6xl mb-4">📈</div>
              <h3 className="text-xl font-bold text-zinc-900 mb-2">开始分析股票</h3>
              <p className="text-zinc-500 mb-4">在上方搜索框输入股票代码或点击热门股票按钮开始</p>
              <div className="text-sm text-zinc-400">
                支持搜索：AAPL (Apple)、MSFT (Microsoft)、TSLA (Tesla) 等
              </div>
            </div>
          </div>
        ) : (
          <>
            <StockChart symbol={selectedSymbol} />
            <FinancialPanel symbol={selectedSymbol} />
          </>
        )}
      </div>
    </div>
  );
}