"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import {
  createChart,
  CandlestickSeries,
  LineSeries,
  HistogramSeries,
  type IChartApi,
  type ISeriesApi,
  type CandlestickData,
  type LineData,
  type HistogramData,
  type Time,
  type IPriceLine,
} from "lightweight-charts";
import { calcMA, calcMACD, calcRSI } from "@/lib/indicators";

type ChartMode = "candlestick" | "line";
type Interval = "1d" | "1wk" | "1mo";
type Range = "1mo" | "6mo" | "2y";

interface HistoricalRow {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

const INTERVAL_RANGE_MAP: Record<Interval, Range> = {
  "1d": "1mo",
  "1wk": "6mo",
  "1mo": "2y",
};

interface StockChartProps {
  symbol: string | null;
}

export default function StockChart({ symbol }: StockChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleSeriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const lineSeriesRef = useRef<ISeriesApi<"Line"> | null>(null);

  const ma5Ref = useRef<ISeriesApi<"Line"> | null>(null);
  const ma10Ref = useRef<ISeriesApi<"Line"> | null>(null);
  const ma20Ref = useRef<ISeriesApi<"Line"> | null>(null);
  const ma60Ref = useRef<ISeriesApi<"Line"> | null>(null);

  const macdContainerRef = useRef<HTMLDivElement>(null);
  const macdChartRef = useRef<IChartApi | null>(null);
  const macdHistRef = useRef<ISeriesApi<"Histogram"> | null>(null);
  const macdDifRef = useRef<ISeriesApi<"Line"> | null>(null);
  const macdDeaRef = useRef<ISeriesApi<"Line"> | null>(null);

  const rsiContainerRef = useRef<HTMLDivElement>(null);
  const rsiChartRef = useRef<IChartApi | null>(null);
  const rsi6Ref = useRef<ISeriesApi<"Line"> | null>(null);
  const rsi14Ref = useRef<ISeriesApi<"Line"> | null>(null);
  const rsi24Ref = useRef<ISeriesApi<"Line"> | null>(null);
  const rsiPriceLinesRef = useRef<IPriceLine[]>([]);

  const [mode, setMode] = useState<ChartMode>("candlestick");
  const [interval, setInterval] = useState<Interval>("1d");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<HistoricalRow[]>([]);

  const [maVisible, setMaVisible] = useState(false);
  const [macdVisible, setMacdVisible] = useState(false);
  const [rsiVisible, setRsiVisible] = useState(false);
  const [chartReady, setChartReady] = useState(false);

  const fetchData = useCallback(async (sym: string, int: Interval) => {
    setLoading(true);
    setError(null);
    try {
      const range = INTERVAL_RANGE_MAP[int];
      const res = await fetch(
        `/api/history?symbol=${encodeURIComponent(sym)}&interval=${int}&range=${range}`
      );
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || "获取数据失败");
      }
      const json: HistoricalRow[] = await res.json();
      setData(json);
    } catch (e) {
      setError(e instanceof Error ? e.message : "获取数据失败");
      setData([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (symbol) {
      fetchData(symbol, interval);
    } else {
      setData([]);
      setError(null);
    }
  }, [symbol, interval, fetchData]);

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      width: containerRef.current.clientWidth,
      height: 500,
      layout: {
        background: { color: "#ffffff" },
        textColor: "#52525b",
      },
      grid: {
        vertLines: { color: "#f4f4f5" },
        horzLines: { color: "#f4f4f5" },
      },
      crosshair: {
        mode: 0,
      },
      timeScale: {
        borderColor: "#e4e4e7",
        timeVisible: true,
        secondsVisible: false,
      },
      rightPriceScale: {
        borderColor: "#e4e4e7",
      },
    });

    chart.timeScale().fitContent();

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: "#ef4444",
      downColor: "#22c55e",
      borderUpColor: "#ef4444",
      borderDownColor: "#22c55e",
      wickUpColor: "#ef4444",
      wickDownColor: "#22c55e",
    });

    const lineSeries = chart.addSeries(LineSeries, {
      color: "#3b82f6",
      lineWidth: 2,
    });

    const ma5 = chart.addSeries(LineSeries, {
      color: "#f59e0b",
      lineWidth: 1,
      visible: false,
    });
    const ma10 = chart.addSeries(LineSeries, {
      color: "#3b82f6",
      lineWidth: 1,
      visible: false,
    });
    const ma20 = chart.addSeries(LineSeries, {
      color: "#ec4899",
      lineWidth: 1,
      visible: false,
    });
    const ma60 = chart.addSeries(LineSeries, {
      color: "#8b5cf6",
      lineWidth: 1,
      visible: false,
    });

    chartRef.current = chart;
    candleSeriesRef.current = candleSeries;
    lineSeriesRef.current = lineSeries;
    ma5Ref.current = ma5;
    ma10Ref.current = ma10;
    ma20Ref.current = ma20;
    ma60Ref.current = ma60;

    setChartReady(true);

    const handleResize = () => {
      if (containerRef.current) {
        chart.applyOptions({ width: containerRef.current.clientWidth });
      }
      if (macdContainerRef.current && macdChartRef.current) {
        macdChartRef.current.applyOptions({
          width: macdContainerRef.current.clientWidth,
        });
      }
      if (rsiContainerRef.current && rsiChartRef.current) {
        rsiChartRef.current.applyOptions({
          width: rsiContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
      chartRef.current = null;
      candleSeriesRef.current = null;
      lineSeriesRef.current = null;
      ma5Ref.current = null;
      ma10Ref.current = null;
      ma20Ref.current = null;
      ma60Ref.current = null;
      setChartReady(false);
    };
  }, []);

  useEffect(() => {
    if (!chartReady || !macdContainerRef.current) return;

    if (macdVisible) {
      const chart = createChart(macdContainerRef.current, {
        width: macdContainerRef.current.clientWidth,
        height: 150,
        layout: {
          background: { color: "#ffffff" },
          textColor: "#52525b",
        },
        grid: {
          vertLines: { color: "#f4f4f5" },
          horzLines: { color: "#f4f4f5" },
        },
        crosshair: {
          mode: 0,
        },
        timeScale: {
          borderColor: "#e4e4e7",
          timeVisible: false,
        },
        rightPriceScale: {
          borderColor: "#e4e4e7",
        },
      });

      const histSeries = chart.addSeries(HistogramSeries, {
        color: "#ef4444",
      });

      const difSeries = chart.addSeries(LineSeries, {
        color: "#3b82f6",
        lineWidth: 1,
      });

      const deaSeries = chart.addSeries(LineSeries, {
        color: "#f59e0b",
        lineWidth: 1,
      });

      macdChartRef.current = chart;
      macdHistRef.current = histSeries;
      macdDifRef.current = difSeries;
      macdDeaRef.current = deaSeries;

      chart.timeScale().fitContent();

      return () => {
        chart.remove();
        macdChartRef.current = null;
        macdHistRef.current = null;
        macdDifRef.current = null;
        macdDeaRef.current = null;
      };
    } else {
      if (macdChartRef.current) {
        macdChartRef.current.remove();
        macdChartRef.current = null;
        macdHistRef.current = null;
        macdDifRef.current = null;
        macdDeaRef.current = null;
      }
    }
  }, [macdVisible, chartReady]);

  useEffect(() => {
    if (!chartReady || !rsiContainerRef.current) return;

    if (rsiVisible) {
      const chart = createChart(rsiContainerRef.current, {
        width: rsiContainerRef.current.clientWidth,
        height: 150,
        layout: {
          background: { color: "#ffffff" },
          textColor: "#52525b",
        },
        grid: {
          vertLines: { color: "#f4f4f5" },
          horzLines: { color: "#f4f4f5" },
        },
        crosshair: {
          mode: 0,
        },
        timeScale: {
          borderColor: "#e4e4e7",
          timeVisible: false,
        },
        rightPriceScale: {
          borderColor: "#e4e4e7",
        },
      });

      const rsi6 = chart.addSeries(LineSeries, {
        color: "#f59e0b",
        lineWidth: 1,
      });

      const rsi14 = chart.addSeries(LineSeries, {
        color: "#3b82f6",
        lineWidth: 1,
      });

      const rsi24 = chart.addSeries(LineSeries, {
        color: "#ec4899",
        lineWidth: 1,
      });

      const line30 = rsi14.createPriceLine({
        price: 30,
        color: "#22c55e",
        lineWidth: 1,
        lineStyle: 2,
        axisLabelVisible: true,
        title: "30",
      });

      const line70 = rsi14.createPriceLine({
        price: 70,
        color: "#ef4444",
        lineWidth: 1,
        lineStyle: 2,
        axisLabelVisible: true,
        title: "70",
      });

      rsiChartRef.current = chart;
      rsi6Ref.current = rsi6;
      rsi14Ref.current = rsi14;
      rsi24Ref.current = rsi24;
      rsiPriceLinesRef.current = [line30, line70];

      chart.timeScale().fitContent();

      return () => {
        chart.remove();
        rsiChartRef.current = null;
        rsi6Ref.current = null;
        rsi14Ref.current = null;
        rsi24Ref.current = null;
        rsiPriceLinesRef.current = [];
      };
    } else {
      if (rsiChartRef.current) {
        rsiChartRef.current.remove();
        rsiChartRef.current = null;
        rsi6Ref.current = null;
        rsi14Ref.current = null;
        rsi24Ref.current = null;
        rsiPriceLinesRef.current = [];
      }
    }
  }, [rsiVisible, chartReady]);

  useEffect(() => {
    const chart = chartRef.current;
    const candleSeries = candleSeriesRef.current;
    const lineSeries = lineSeriesRef.current;

    if (!chart || !candleSeries || !lineSeries) return;

    if (data.length === 0) {
      candleSeries.setData([]);
      lineSeries.setData([]);
      return;
    }

    const timeData: Time[] = data.map(
      (row) => (row.date as string).split("T")[0] as Time
    );

    const candleData: CandlestickData<Time>[] = data.map((row, i) => ({
      time: timeData[i],
      open: row.open,
      high: row.high,
      low: row.low,
      close: row.close,
    }));

    const lineData: LineData<Time>[] = data.map((row, i) => ({
      time: timeData[i],
      value: row.close,
    }));

    candleSeries.setData(candleData);
    lineSeries.setData(lineData);

    if (mode === "candlestick") {
      candleSeries.applyOptions({ visible: true });
      lineSeries.applyOptions({ visible: false });
    } else {
      candleSeries.applyOptions({ visible: false });
      lineSeries.applyOptions({ visible: true });
    }

    const ma5 = ma5Ref.current;
    const ma10 = ma10Ref.current;
    const ma20 = ma20Ref.current;
    const ma60 = ma60Ref.current;

    if (ma5 && ma10 && ma20 && ma60) {
      const closePrices = data.map((row) => row.close);
      const ma5Vals = calcMA(closePrices, 5);
      const ma10Vals = calcMA(closePrices, 10);
      const ma20Vals = calcMA(closePrices, 20);
      const ma60Vals = calcMA(closePrices, 60);

      ma5.setData(
        ma5Vals
          .map((v, i) => (v !== null ? { time: timeData[i], value: v } : null))
          .filter((d): d is LineData<Time> => d !== null)
      );
      ma10.setData(
        ma10Vals
          .map((v, i) => (v !== null ? { time: timeData[i], value: v } : null))
          .filter((d): d is LineData<Time> => d !== null)
      );
      ma20.setData(
        ma20Vals
          .map((v, i) => (v !== null ? { time: timeData[i], value: v } : null))
          .filter((d): d is LineData<Time> => d !== null)
      );
      ma60.setData(
        ma60Vals
          .map((v, i) => (v !== null ? { time: timeData[i], value: v } : null))
          .filter((d): d is LineData<Time> => d !== null)
      );
    }

    if (macdChartRef.current) {
      const macdChart = macdChartRef.current;
      const histSeries = macdHistRef.current;
      const difSeries = macdDifRef.current;
      const deaSeries = macdDeaRef.current;

      if (histSeries && difSeries && deaSeries) {
        const closePrices = data.map((row) => row.close);
        const macd = calcMACD(closePrices);

        const histData: HistogramData<Time>[] = [];
        const difData: LineData<Time>[] = [];
        const deaData: LineData<Time>[] = [];

        for (let i = 0; i < macd.histogram.length; i++) {
          const h = macd.histogram[i];
          const d = macd.dif[i];
          const de = macd.dea[i];
          if (h !== null) {
            histData.push({ time: timeData[i], value: h, color: h >= 0 ? "#ef4444" : "#22c55e" });
          }
          if (d !== null) {
            difData.push({ time: timeData[i], value: d });
          }
          if (de !== null) {
            deaData.push({ time: timeData[i], value: de });
          }
        }

        histSeries.setData(histData);
        difSeries.setData(difData);
        deaSeries.setData(deaData);
        macdChart.timeScale().fitContent();
      }
    }

    if (rsiChartRef.current) {
      const rsiChart = rsiChartRef.current;
      const r6 = rsi6Ref.current;
      const r14 = rsi14Ref.current;
      const r24 = rsi24Ref.current;

      if (r6 && r14 && r24) {
        const closePrices = data.map((row) => row.close);
        const rsi6Vals = calcRSI(closePrices, 6);
        const rsi14Vals = calcRSI(closePrices, 14);
        const rsi24Vals = calcRSI(closePrices, 24);

        r6.setData(
          rsi6Vals
            .map((v, i) => (v !== null ? { time: timeData[i], value: v } : null))
            .filter((d): d is LineData<Time> => d !== null)
        );
        r14.setData(
          rsi14Vals
            .map((v, i) => (v !== null ? { time: timeData[i], value: v } : null))
            .filter((d): d is LineData<Time> => d !== null)
        );
        r24.setData(
          rsi24Vals
            .map((v, i) => (v !== null ? { time: timeData[i], value: v } : null))
            .filter((d): d is LineData<Time> => d !== null)
        );
        rsiChart.timeScale().fitContent();
      }
    }

    chart.timeScale().fitContent();
  }, [data, mode]);

  useEffect(() => {
    const ma5 = ma5Ref.current;
    const ma10 = ma10Ref.current;
    const ma20 = ma20Ref.current;
    const ma60 = ma60Ref.current;

    if (ma5) ma5.applyOptions({ visible: maVisible });
    if (ma10) ma10.applyOptions({ visible: maVisible });
    if (ma20) ma20.applyOptions({ visible: maVisible });
    if (ma60) ma60.applyOptions({ visible: maVisible });
  }, [maVisible]);

  const intervals: { label: string; value: Interval }[] = [
    { label: "日K", value: "1d" },
    { label: "周K", value: "1wk" },
    { label: "月K", value: "1mo" },
  ];

  const modeButtons: { label: string; value: ChartMode }[] = [
    { label: "K线图", value: "candlestick" },
    { label: "折线图", value: "line" },
  ];

  const indicatorButtons = [
    { label: "MA", value: "ma" as const, visible: maVisible, setter: setMaVisible },
    { label: "MACD", value: "macd" as const, visible: macdVisible, setter: setMacdVisible },
    { label: "RSI", value: "rsi" as const, visible: rsiVisible, setter: setRsiVisible },
  ];

  const buttonClass = (active: boolean) =>
    `px-4 py-2 text-sm rounded-md border transition-colors min-h-[44px] min-w-[44px] ${
      active
        ? "border-blue-500 bg-blue-50 text-blue-700"
        : "border-zinc-300 bg-white text-zinc-600 hover:bg-zinc-50 active:bg-zinc-100"
    }`;

  if (!symbol) {
    return (
      <main className="flex-1 min-h-[500px] rounded-lg border border-zinc-200 bg-white p-4 flex items-center justify-center">
        <p className="text-sm text-zinc-400">请输入股票代码查看图表</p>
      </main>
    );
  }

  return (
    <main className="flex-1 rounded-lg border border-zinc-200 bg-white p-4 flex flex-col min-h-0">
      <div className="flex items-center justify-between mb-3 gap-2 flex-wrap">
        <div className="flex items-center gap-1">
          {modeButtons.map((btn) => (
            <button
              key={btn.value}
              onClick={() => setMode(btn.value)}
              className={buttonClass(mode === btn.value)}
            >
              {btn.label}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-1">
          {indicatorButtons.map((btn) => (
            <button
              key={btn.value}
              onClick={() => btn.setter((prev) => !prev)}
              className={buttonClass(btn.visible)}
            >
              {btn.label}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-1">
          {intervals.map((item) => (
            <button
              key={item.value}
              onClick={() => setInterval(item.value)}
              className={buttonClass(interval === item.value)}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>
      <div className="relative flex flex-col flex-1 min-h-0">
        {loading && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-white/70">
            <span className="text-sm text-zinc-500">加载中...</span>
          </div>
        )}
        {error && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-white/70">
            <span className="text-sm text-red-500">{error}</span>
          </div>
        )}
        <div ref={containerRef} className="w-full" style={{ height: 500, minHeight: 500 }} />
        {macdVisible && (
          <div ref={macdContainerRef} className="w-full" style={{ height: 150 }} />
        )}
        {rsiVisible && (
          <div ref={rsiContainerRef} className="w-full" style={{ height: 150 }} />
        )}
      </div>
    </main>
  );
}