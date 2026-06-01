"use client";

import { useEffect, useState } from "react";

interface QuoteData {
  longName?: string;
  shortName?: string;
  regularMarketPrice?: number;
  regularMarketChange?: number;
  regularMarketChangePercent?: number;
  marketCap?: number;
  trailingPE?: number;
  trailingEps?: number;
  trailingAnnualDividendYield?: number;
  fiftyTwoWeekHigh?: number;
  fiftyTwoWeekLow?: number;
  regularMarketVolume?: number;
  averageDailyVolume3Month?: number;
}

interface FinancialPanelProps {
  symbol: string | null;
}

function fmtMarketCap(value: number): string {
  if (value >= 1e12) {
    return (value / 1e12).toFixed(2) + " 万亿";
  }
  if (value >= 1e8) {
    return (value / 1e8).toFixed(2) + " 亿";
  }
  if (value >= 1e4) {
    return (value / 1e4).toFixed(2) + " 万";
  }
  return value.toLocaleString();
}

function fmtVolume(value: number): string {
  if (value >= 1e8) {
    return (value / 1e8).toFixed(2) + " 亿";
  }
  if (value >= 1e4) {
    return (value / 1e4).toFixed(2) + " 万";
  }
  return value.toLocaleString();
}

function MetricRow({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-zinc-100 last:border-b-0">
      <span className="text-sm text-zinc-500">{label}</span>
      <span className="text-sm font-medium text-zinc-900">{children}</span>
    </div>
  );
}

export default function FinancialPanel({ symbol }: FinancialPanelProps) {
  const [data, setData] = useState<QuoteData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!symbol) {
      setData(null);
      setError(null);
      return;
    }

    const currentSymbol = symbol;
    let cancelled = false;

    async function fetchQuote() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`/api/quote?symbol=${encodeURIComponent(currentSymbol)}`);
        if (!res.ok) {
          const body = await res.json();
          throw new Error(body.error || "获取数据失败");
        }
        const json = await res.json();
        if (!cancelled) {
          setData(json);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "获取数据失败");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchQuote();

    return () => {
      cancelled = true;
    };
  }, [symbol]);

  if (!symbol) {
    return (
      <aside className="w-full md:w-80 rounded-lg border border-zinc-200 bg-white p-3 md:p-4">
        <p className="text-sm text-zinc-400 text-center py-8">请选择股票</p>
      </aside>
    );
  }

  if (loading) {
    return (
      <aside className="w-full md:w-80 rounded-lg border border-zinc-200 bg-white p-3 md:p-4">
        <div className="flex items-center justify-center py-8">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-300 border-t-blue-500" />
        </div>
      </aside>
    );
  }

  if (error) {
    return (
      <aside className="w-full md:w-80 rounded-lg border border-zinc-200 bg-white p-3 md:p-4">
        <p className="text-sm text-red-500 text-center py-8">{error}</p>
      </aside>
    );
  }

  if (!data) {
    return (
      <aside className="w-full md:w-80 rounded-lg border border-zinc-200 bg-white p-3 md:p-4">
        <p className="text-sm text-zinc-400 text-center py-8">暂无数据</p>
      </aside>
    );
  }

  const name = data.longName || data.shortName || symbol;
  const price = data.regularMarketPrice;
  const change = data.regularMarketChange;
  const changePercent = data.regularMarketChangePercent;
  const isUp = change != null && change >= 0;
  const changeColor = isUp ? "text-red-500" : "text-green-500";

  return (
    <aside className="w-full md:w-80 rounded-lg border border-zinc-200 bg-white p-3 md:p-4">
      <h2 className="text-base font-bold text-zinc-900 mb-3 truncate" title={name}>
        {name}
      </h2>
      <div className="space-y-0">
        {price != null && (
          <MetricRow label="当前价格">
            <span className={changeColor}>
              {price.toFixed(2)}
              {change != null && (
                <span className="ml-1.5 text-xs">
                  {isUp ? "+" : ""}
                  {change.toFixed(2)}
                  {changePercent != null && (
                    <span>
                      {" "}
                      ({isUp ? "+" : ""}
                      {(changePercent * 100).toFixed(2)}%)
                    </span>
                  )}
                </span>
              )}
            </span>
          </MetricRow>
        )}
        {data.marketCap != null && (
          <MetricRow label="市值">
            {fmtMarketCap(data.marketCap)}
          </MetricRow>
        )}
        {data.trailingPE != null && (
          <MetricRow label="市盈率 PE">
            {data.trailingPE.toFixed(2)}
          </MetricRow>
        )}
        {data.trailingEps != null && (
          <MetricRow label="每股收益 EPS">
            {data.trailingEps.toFixed(2)}
          </MetricRow>
        )}
        {data.trailingAnnualDividendYield != null && (
          <MetricRow label="股息率">
            {(data.trailingAnnualDividendYield * 100).toFixed(2)}%
          </MetricRow>
        )}
        {data.fiftyTwoWeekHigh != null && (
          <MetricRow label="52周最高">
            {data.fiftyTwoWeekHigh.toFixed(2)}
          </MetricRow>
        )}
        {data.fiftyTwoWeekLow != null && (
          <MetricRow label="52周最低">
            {data.fiftyTwoWeekLow.toFixed(2)}
          </MetricRow>
        )}
        {data.regularMarketVolume != null && (
          <MetricRow label="成交量">
            {fmtVolume(data.regularMarketVolume)}
          </MetricRow>
        )}
        {data.averageDailyVolume3Month != null && (
          <MetricRow label="平均成交量">
            {fmtVolume(data.averageDailyVolume3Month)}
          </MetricRow>
        )}
      </div>
    </aside>
  );
}