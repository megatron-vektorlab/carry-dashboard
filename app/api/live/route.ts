import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

// Universe: coins with USDT perps on Binance (funding chips from Bybit/Hyperliquid
// appear when the venue lists the coin; missing venues degrade gracefully).
const COINS = [
  "BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "LINK",
  "AVAX", "LTC", "DOT", "TRX", "BCH", "NEAR",
  "SUI", "TON", "APT", "ARB", "OP", "FIL", "ATOM", "UNI",
];

async function j(url: string, init?: RequestInit) {
  const r = await fetch(url, {
    ...init,
    signal: AbortSignal.timeout(9000),
    cache: "no-store",
    headers: { "User-Agent": "carry-radar", "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

type CoinAgg = {
  funding: Record<string, number>; // venue -> annualized funding %
  price?: number;
  mark?: number;
  chg24h?: number;
  spark?: number[];
};

export async function GET() {
  const agg: Record<string, CoinAgg> = {};
  for (const c of COINS) agg[c] = { funding: {} };
  const venuesOk: Record<string, boolean> = { binance: false, bybit: false, hyperliquid: false };

  await Promise.all([
    // Binance USD-M: funding + mark price, one call
    (async () => {
      try {
        const arr = await j("https://fapi.binance.com/fapi/v1/premiumIndex");
        for (const x of arr) {
          const s: string = x.symbol ?? "";
          if (!s.endsWith("USDT")) continue;
          const c = s.slice(0, -4);
          if (!agg[c]) continue;
          agg[c].funding.binance = parseFloat(x.lastFundingRate) * 3 * 365 * 100;
          agg[c].mark = parseFloat(x.markPrice);
        }
        venuesOk.binance = true;
      } catch {}
    })(),
    // Binance USD-M: 24h price/change, one call
    (async () => {
      try {
        const arr = await j("https://fapi.binance.com/fapi/v1/ticker/24hr");
        for (const x of arr) {
          const s: string = x.symbol ?? "";
          if (!s.endsWith("USDT")) continue;
          const c = s.slice(0, -4);
          if (!agg[c]) continue;
          agg[c].price = parseFloat(x.lastPrice);
          agg[c].chg24h = parseFloat(x.priceChangePercent);
        }
      } catch {}
    })(),
    // Bybit linear: funding, one call
    (async () => {
      try {
        const r = await j("https://api.bybit.com/v5/market/tickers?category=linear");
        for (const x of r?.result?.list ?? []) {
          const s: string = x.symbol ?? "";
          if (!s.endsWith("USDT")) continue;
          const c = s.slice(0, -4);
          if (!agg[c] || x.fundingRate === "" || x.fundingRate == null) continue;
          agg[c].funding.bybit = parseFloat(x.fundingRate) * 3 * 365 * 100;
        }
        venuesOk.bybit = true;
      } catch {}
    })(),
    // Hyperliquid: hourly funding, one call
    (async () => {
      try {
        const [meta, ctxs] = await j("https://api.hyperliquid.xyz/info", {
          method: "POST",
          body: JSON.stringify({ type: "metaAndAssetCtxs" }),
        });
        (meta?.universe ?? []).forEach((u: any, i: number) => {
          const c = u?.name;
          const f = ctxs?.[i]?.funding;
          if (c && agg[c] && f != null) {
            agg[c].funding.hyperliquid = parseFloat(f) * 24 * 365 * 100;
          }
        });
        venuesOk.hyperliquid = true;
      } catch {}
    })(),
  ]);

  // Sparklines: 7 days of 2h closes per coin (Binance USD-M)
  await Promise.all(
    COINS.map(async (c) => {
      if (agg[c].price == null && agg[c].mark == null) return;
      try {
        const arr = await j(`https://fapi.binance.com/fapi/v1/klines?symbol=${c}USDT&interval=2h&limit=84`);
        agg[c].spark = arr.map((k: any[]) => parseFloat(k[4]));
      } catch {}
    })
  );

  const coins = COINS.filter((c) => agg[c].price != null || agg[c].mark != null).map((c) => {
    const f = agg[c].funding;
    let bestVenue: string | null = null;
    for (const v of Object.keys(f)) {
      if (bestVenue === null || f[v] > f[bestVenue]) bestVenue = v;
    }
    return {
      c,
      price: agg[c].price ?? agg[c].mark ?? null,
      chg24h: agg[c].chg24h ?? null,
      spark: agg[c].spark ?? [],
      funding: f,
      bestVenue,
      bestApy: bestVenue ? f[bestVenue] : null,
    };
  });
  coins.sort((a, b) => (b.bestApy ?? -1e9) - (a.bestApy ?? -1e9));

  return NextResponse.json(
    { t: Date.now(), venuesOk, coins },
    { headers: { "Cache-Control": "s-maxage=45, stale-while-revalidate=90" } }
  );
}
