"use client";

import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import StockChart from "@/components/StockChart";
import FinancialPanel from "@/components/FinancialPanel";

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
        <div className="max-w-7xl mx-auto px-3 md:px-4 py-4">
          <SearchBar onSelect={handleSelect} />
        </div>
      </div>
      {selectedSymbol && selectedName && (
        <div className="max-w-7xl mx-auto w-full px-3 md:px-4 pt-4">
          <h2 className="text-lg font-bold text-zinc-900">
            {selectedSymbol}
            <span className="ml-2 text-sm font-normal text-zinc-500">
              {selectedName}
            </span>
          </h2>
        </div>
      )}
      <div className="flex flex-1 max-w-7xl mx-auto w-full flex-col md:flex-row gap-4 md:gap-6 px-3 md:px-4 py-4 md:py-6">
        <StockChart symbol={selectedSymbol} />
        <FinancialPanel symbol={selectedSymbol} />
      </div>
    </div>
  );
}