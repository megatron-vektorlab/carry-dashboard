import { NextResponse } from "next/server";
import fs from "node:fs";
import path from "node:path";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const dir = path.join(process.cwd(), "data");
    const state = JSON.parse(fs.readFileSync(path.join(dir, "paper_state.json"), "utf8"));
    const lines = fs
      .readFileSync(path.join(dir, "paper_history.csv"), "utf8")
      .trim()
      .split(/\r?\n/);
    const history = lines.slice(1).map((l) => {
      const p = l.split(",");
      return { t: p[0], equity: parseFloat(p[1]) };
    });

    // Optional ML rotation experiment (race vs carry)
    let ml: { state: any; history: { t: string; equity: number }[] } | null = null;
    try {
      const mlState = JSON.parse(fs.readFileSync(path.join(dir, "ml_portfolio.json"), "utf8"));
      const mlLines = fs
        .readFileSync(path.join(dir, "ml_history.csv"), "utf8")
        .trim()
        .split(/\r?\n/);
      const mlHistory = mlLines.slice(1).map((l) => {
        const p = l.split(",");
        return { t: p[0], equity: parseFloat(p[1]) };
      });
      ml = {
        state: {
          equity: mlState.current_value_usd,
          initial: mlState.initial_usd,
          symbol: mlState.current_symbol,
          trades: mlState.total_trades,
          fees: mlState.total_fees_paid,
          started_at: mlState.started_at,
        },
        history: mlHistory,
      };
    } catch {}

    return NextResponse.json({ state, history, ml });
  } catch (e) {
    return NextResponse.json({ error: String(e) }, { status: 500 });
  }
}
