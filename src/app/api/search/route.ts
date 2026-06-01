import { NextResponse } from "next/server";
import { searchStocks } from "@/lib/api";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("q");

  if (!query) {
    return NextResponse.json(
      { error: '缺少查询参数 "q"' },
      { status: 400 }
    );
  }

  try {
    const results = await searchStocks(query);
    return NextResponse.json(results);
  } catch (error) {
    console.error("搜索失败:", error);
    return NextResponse.json(
      { error: "搜索股票失败，请稍后重试" },
      { status: 500 }
    );
  }
}