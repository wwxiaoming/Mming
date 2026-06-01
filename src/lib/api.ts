import YahooFinance from "yahoo-finance2";

const mockStocks = [
  { symbol: "AAPL", shortname: "Apple Inc.", longname: "Apple Inc." },
  { symbol: "MSFT", shortname: "Microsoft Corporation", longname: "Microsoft Corporation" },
  { symbol: "GOOGL", shortname: "Alphabet Inc.", longname: "Alphabet Inc." },
  { symbol: "AMZN", shortname: "Amazon.com Inc.", longname: "Amazon.com Inc." },
  { symbol: "TSLA", shortname: "Tesla Inc.", longname: "Tesla Inc." },
  { symbol: "META", shortname: "Meta Platforms Inc.", longname: "Meta Platforms Inc." },
  { symbol: "NVDA", shortname: "NVIDIA Corporation", longname: "NVIDIA Corporation" },
  { symbol: "JPM", shortname: "JPMorgan Chase & Co.", longname: "JPMorgan Chase & Co." },
  { symbol: "V", shortname: "Visa Inc.", longname: "Visa Inc." },
  { symbol: "JNJ", shortname: "Johnson & Johnson", longname: "Johnson & Johnson" },
  { symbol: "WMT", shortname: "Walmart Inc.", longname: "Walmart Inc." },
  { symbol: "PG", shortname: "Procter & Gamble Co.", longname: "Procter & Gamble Co." },
  { symbol: "BAC", shortname: "Bank of America Corp.", longname: "Bank of America Corp." },
  { symbol: "ADBE", shortname: "Adobe Inc.", longname: "Adobe Inc." },
  { symbol: "NFLX", shortname: "Netflix Inc.", longname: "Netflix Inc." },
  { symbol: "KO", shortname: "Coca-Cola Co.", longname: "Coca-Cola Co." },
  { symbol: "PEP", shortname: "PepsiCo Inc.", longname: "PepsiCo Inc." },
  { symbol: "INTC", shortname: "Intel Corporation", longname: "Intel Corporation" },
  { symbol: "AMD", shortname: "Advanced Micro Devices", longname: "Advanced Micro Devices Inc." },
  { symbol: "ORCL", shortname: "Oracle Corporation", longname: "Oracle Corporation" },
];

function generateMockQuote(symbol: string) {
  const basePrice = 100 + Math.random() * 400;
  const change = (Math.random() - 0.5) * 10;
  return {
    symbol,
    regularMarketPrice: basePrice,
    regularMarketChange: change,
    regularMarketChangePercent: (change / basePrice) * 100,
    regularMarketPreviousClose: basePrice - change,
    regularMarketOpen: basePrice - change + (Math.random() - 0.5) * 2,
    regularMarketDayHigh: basePrice + Math.random() * 5,
    regularMarketDayLow: basePrice - Math.random() * 5,
    regularMarketVolume: Math.floor(Math.random() * 50000000) + 1000000,
    marketCap: Math.floor(Math.random() * 3000000000000) + 100000000000,
  };
}

function generateMockHistory(symbol: string, range: string) {
  const data = [];
  const now = new Date();
  let days = 365;
  
  switch (range) {
    case "1d": days = 1; break;
    case "5d": days = 5; break;
    case "1mo": days = 30; break;
    case "3mo": days = 90; break;
    case "6mo": days = 180; break;
    case "1y": days = 365; break;
    case "2y": days = 730; break;
    case "5y": days = 1825; break;
    default: days = 365;
  }

  let price = 100 + Math.random() * 200;
  for (let i = days; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    
    const change = (Math.random() - 0.48) * 4;
    price = Math.max(price + change, 10);
    
    data.push({
      date,
      open: price - (Math.random() - 0.5) * 2,
      high: price + Math.random() * 3,
      low: price - Math.random() * 3,
      close: price,
      volume: Math.floor(Math.random() * 50000000) + 1000000,
    });
  }
  
  return data;
}

export async function searchStocks(query: string) {
  try {
    const yahooFinance = new YahooFinance();
    return await yahooFinance.search(query, { quotesCount: 10, newsCount: 0 });
  } catch (error) {
    console.log("使用模拟搜索数据，Yahoo Finance 不可访问");
    const lowerQuery = query.toLowerCase();
    const filtered = mockStocks.filter(
      s => s.symbol.toLowerCase().includes(lowerQuery) || 
           s.shortname?.toLowerCase().includes(lowerQuery) ||
           s.longname?.toLowerCase().includes(lowerQuery)
    );
    return { quotes: filtered.slice(0, 10) };
  }
}

export async function getHistoricalData(
  symbol: string,
  interval: string,
  range: string
) {
  try {
    const yahooFinance = new YahooFinance();
    const now = new Date();
    const period1 = getStartDate(range);

    const validIntervals = ["1d", "1wk", "1mo"];
    const resolvedInterval = validIntervals.includes(interval)
      ? (interval as "1d" | "1wk" | "1mo")
      : "1d";

    return await yahooFinance.historical(symbol, {
      period1,
      period2: now,
      interval: resolvedInterval,
    });
  } catch (error) {
    console.log("使用模拟历史数据，Yahoo Finance 不可访问");
    return generateMockHistory(symbol, range);
  }
}

export async function getQuote(symbol: string) {
  try {
    const yahooFinance = new YahooFinance();
    return await yahooFinance.quote(symbol);
  } catch (error) {
    console.log("使用模拟报价数据，Yahoo Finance 不可访问");
    return generateMockQuote(symbol);
  }
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