import { NextResponse } from "next/server";
import { getHistoricalData } from "@/lib/api";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const symbol = searchParams.get("symbol");
  const interval = searchParams.get("interval") || "1d";
  const range = searchParams.get("range") || "1mo";

  if (!symbol) {
    return NextResponse.json(
      { error: '缺少查询参数 "symbol"' },
      { status: 400 }
    );
  }

  try {
    const results = await getHistoricalData(symbol, interval, range);
    return NextResponse.json(results);
  } catch (error) {
    console.error("获取历史数据失败:", error);
    return NextResponse.json(
      { error: "获取历史数据失败，请稍后重试" },
      { status: 500 }
    );
  }
}