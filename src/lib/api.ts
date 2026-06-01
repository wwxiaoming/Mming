import YahooFinance from "yahoo-finance2";

export async function searchStocks(query: string) {
  const yahooFinance = new YahooFinance();
  return yahooFinance.search(query, { quotesCount: 10, newsCount: 0 });
}

export async function getHistoricalData(
  symbol: string,
  interval: string,
  range: string
) {
  const yahooFinance = new YahooFinance();
  const now = new Date();
  const period1 = getStartDate(range);

  const validIntervals = ["1d", "1wk", "1mo"];
  const resolvedInterval = validIntervals.includes(interval)
    ? (interval as "1d" | "1wk" | "1mo")
    : "1d";

  return yahooFinance.historical(symbol, {
    period1,
    period2: now,
    interval: resolvedInterval,
  });
}

export async function getQuote(symbol: string) {
  const yahooFinance = new YahooFinance();
  return yahooFinance.quote(symbol);
}

function getStartDate(range: string): Date {
  const now = new Date();
  switch (range) {
    case "1d":
      return new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000);
    case "5d":
      return new Date(now.getTime() - 5 * 24 * 60 * 60 * 1000);
    case "1mo":
      return new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
    case "3mo":
      return new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000);
    case "6mo":
      return new Date(now.getTime() - 180 * 24 * 60 * 60 * 1000);
    case "1y":
      return new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
    case "2y":
      return new Date(now.getTime() - 2 * 365 * 24 * 60 * 60 * 1000);
    case "5y":
      return new Date(now.getTime() - 5 * 365 * 24 * 60 * 60 * 1000);
    case "max":
      return new Date(0);
    default:
      return new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
  }
}