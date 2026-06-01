"use client";

import { useState, useEffect, useRef } from "react";

interface StockSuggestion {
  symbol: string;
  name: string;
}

interface SearchBarProps {
  onSelect: (symbol: string, name: string) => void;
}

export default function SearchBar({ onSelect }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState<StockSuggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // 搜索建议
  useEffect(() => {
    if (!query.trim()) {
      setSuggestions([]);
      setIsOpen(false);
      return;
    }

    const fetchSuggestions = async () => {
      setIsLoading(true);
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        if (data.quotes && data.quotes.length > 0) {
          const mapped: StockSuggestion[] = data.quotes
            .filter((q: any) => q.symbol)
            .map((q: any) => ({
              symbol: q.symbol,
              name: q.shortname || q.longname || q.symbol,
            }));
          setSuggestions(mapped);
        } else {
          setSuggestions([]);
        }
        setIsOpen(true);
      } catch (err) {
        console.error("搜索失败", err);
        setSuggestions([]);
      } finally {
        setIsLoading(false);
      }
    };

    const timer = setTimeout(fetchSuggestions, 300);
    return () => clearTimeout(timer);
  }, [query]);

  // 点击外部关闭
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // 选择股票
  const handleSelect = (suggestion: StockSuggestion) => {
    onSelect(suggestion.symbol, suggestion.name);
    setQuery(suggestion.symbol);
    setIsOpen(false);
  };

  // 提交搜索
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    if (suggestions.length > 0) {
      handleSelect(suggestions[0]);
    } else {
      onSelect(query.trim().toUpperCase(), query.trim());
      setIsOpen(false);
    }
  };

  return (
    <div ref={containerRef} className="relative">
      <form onSubmit={handleSubmit} className="flex gap-3">
        <div className="relative flex-1">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg className="h-5 w-5 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => {
              if (suggestions.length > 0 || query.trim()) {
                setIsOpen(true);
              }
            }}
            placeholder="搜索股票代码或名称，如 AAPL、MSFT、Tesla..."
            className="w-full rounded-xl border-2 border-zinc-300 pl-12 pr-4 py-4 text-lg focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition-all shadow-sm"
          />
        </div>
        <button
          type="submit"
          disabled={!query.trim()}
          className="px-6 py-4 bg-blue-600 text-white rounded-xl font-medium text-lg hover:bg-blue-700 active:bg-blue-800 disabled:bg-zinc-300 disabled:cursor-not-allowed transition-all shadow-md min-w-[100px]"
        >
          搜索
        </button>
      </form>

      {isOpen && (
        <div className="absolute z-50 mt-1 w-full" style={{ maxWidth: 'calc(100% - 116px)' }}>
          <div className="rounded-lg border border-zinc-200 bg-white shadow-lg">
            {isLoading && (
              <div className="px-4 py-3 text-sm text-zinc-500">搜索中...</div>
            )}
            
            {!isLoading && suggestions.length === 0 && query.trim() && (
              <div className="px-4 py-3 text-sm text-zinc-400">未找到匹配的股票</div>
            )}

            {!isLoading && suggestions.length > 0 && (
              <ul className="max-h-60 overflow-auto py-1">
                {suggestions.map((s) => (
                  <li
                    key={s.symbol}
                    onClick={() => handleSelect(s)}
                    className="flex items-center gap-3 px-4 py-3 cursor-pointer text-sm hover:bg-zinc-50 active:bg-blue-50"
                  >
                    <span className="font-semibold text-zinc-900 min-w-[80px]">{s.symbol}</span>
                    <span className="text-zinc-500 truncate">{s.name}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
