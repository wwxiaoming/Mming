"use client";

import { useState, useEffect, useRef, useCallback } from "react";

interface StockSuggestion {
  symbol: string;
  name: string;
}

interface SearchApiResponse {
  quotes?: Array<{
    symbol?: string;
    shortname?: string;
    longname?: string;
  }>;
  error?: string;
}

interface SearchBarProps {
  onSelect: (symbol: string, name: string) => void;
}

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}

export default function SearchBar({ onSelect }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState<StockSuggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);

  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (!debouncedQuery.trim()) {
      setSuggestions([]);
      setIsOpen(false);
      setError(null);
      return;
    }

    const fetchSuggestions = async () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

      const controller = new AbortController();
      abortControllerRef.current = controller;

      setIsLoading(true);
      setError(null);

      try {
        const res = await fetch(
          `/api/search?q=${encodeURIComponent(debouncedQuery)}`,
          { signal: controller.signal }
        );

        if (!res.ok) {
          const data = await res.json();
          throw new Error(data.error || "搜索失败");
        }

        const data: SearchApiResponse = await res.json();

        if (data.quotes && data.quotes.length > 0) {
          const mapped: StockSuggestion[] = data.quotes
            .filter((q) => q.symbol)
            .map((q) => ({
              symbol: q.symbol!,
              name: q.shortname || q.longname || q.symbol!,
            }));
          setSuggestions(mapped);
          setIsOpen(true);
        } else {
          setSuggestions([]);
          setIsOpen(true);
        }
      } catch (err: unknown) {
        if (err instanceof DOMException && err.name === "AbortError") {
          return;
        }
        setError(err instanceof Error ? err.message : "搜索失败");
        setSuggestions([]);
        setIsOpen(true);
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      }
    };

    fetchSuggestions();

    return () => {
      abortControllerRef.current?.abort();
    };
  }, [debouncedQuery]);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleSelect = useCallback(
    (suggestion: StockSuggestion) => {
      onSelect(suggestion.symbol, suggestion.name);
      setQuery(suggestion.symbol);
      setIsOpen(false);
      setHighlightedIndex(-1);
    },
    [onSelect]
  );

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!isOpen || suggestions.length === 0) {
      if (e.key === "Enter" && query.trim()) {
        handleSelect({ symbol: query.trim().toUpperCase(), name: query.trim() });
      }
      return;
    }

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setHighlightedIndex((prev) =>
          prev < suggestions.length - 1 ? prev + 1 : 0
        );
        break;
      case "ArrowUp":
        e.preventDefault();
        setHighlightedIndex((prev) =>
          prev > 0 ? prev - 1 : suggestions.length - 1
        );
        break;
      case "Enter":
        e.preventDefault();
        if (highlightedIndex >= 0 && highlightedIndex < suggestions.length) {
          handleSelect(suggestions[highlightedIndex]);
        } else if (suggestions.length > 0) {
          handleSelect(suggestions[0]);
        }
        break;
      case "Escape":
        setIsOpen(false);
        setHighlightedIndex(-1);
        inputRef.current?.blur();
        break;
    }
  };

  const highlightMatch = (text: string) => {
    if (!query.trim()) return text;

    const parts = text.split(new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`, "gi"));
    return parts.map((part, i) =>
      part.toLowerCase() === query.toLowerCase() ? (
        <mark key={i} className="bg-yellow-200 text-inherit rounded-sm px-0.5">
          {part}
        </mark>
      ) : (
        part
      )
    );
  };

  return (
    <div ref={containerRef} className="relative">
      <input
        ref={inputRef}
        type="text"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setHighlightedIndex(-1);
        }}
        onKeyDown={handleKeyDown}
        onFocus={() => {
          if (suggestions.length > 0 || error) {
            setIsOpen(true);
          }
        }}
        placeholder="搜索股票代码或名称..."
        className="w-full rounded-lg border border-zinc-300 px-3 md:px-4 py-2.5 text-base focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      />

      {isOpen && (
        <div className="absolute z-50 mt-1 w-full rounded-lg border border-zinc-200 bg-white shadow-lg">
          {isLoading && (
            <div className="flex items-center gap-2 px-4 py-3 text-sm text-zinc-500">
              <svg
                className="h-4 w-4 animate-spin"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              搜索中...
            </div>
          )}

          {!isLoading && error && (
            <div className="px-4 py-3 text-sm text-red-500">{error}</div>
          )}

          {!isLoading && !error && suggestions.length === 0 && (
            <div className="px-4 py-3 text-sm text-zinc-400">
              未找到匹配的股票
            </div>
          )}

          {!isLoading && !error && suggestions.length > 0 && (
            <ul className="max-h-60 overflow-auto py-1">
              {suggestions.map((s, index) => (
                <li
                  key={s.symbol}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    handleSelect(s);
                  }}
                  onClick={(e) => {
                    e.preventDefault();
                    handleSelect(s);
                  }}
                  onTouchStart={(e) => {
                    setHighlightedIndex(index);
                  }}
                  onTouchEnd={(e) => {
                    e.preventDefault();
                    handleSelect(s);
                  }}
                  onMouseEnter={() => setHighlightedIndex(index)}
                  className={`flex items-center gap-3 px-4 py-3 cursor-pointer text-sm active:bg-blue-50 ${
                    index === highlightedIndex
                      ? "bg-blue-50 text-blue-700"
                      : "hover:bg-zinc-50"
                  }`}
                >
                  <span className="font-semibold text-zinc-900 min-w-[80px]">
                    {highlightMatch(s.symbol)}
                  </span>
                  <span className="text-zinc-500 truncate">
                    {highlightMatch(s.name)}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}