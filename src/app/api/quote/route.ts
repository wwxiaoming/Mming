import { NextResponse } from "next/server";
import { getQuote } from "@/lib/api";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const symbol = searchParams.get("symbol");

  if (!symbol) {
    return NextResponse.json(
      { error: '缺少查询参数 "symbol"' },
      { status: 400 }
    );
  }

  try {
    const results = await getQuote(symbol);
    return NextResponse.json(results);
  } catch (error) {
    console.error("获取报价失败:", error);
    return NextResponse.json(
      { error: "获取报价数据失败，请稍后重试" },
      { status: 500 }
    );
  }
}