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
    return NextResponse.json({ state, history });
  } catch (e) {
    return NextResponse.json({ error: String(e) }, { status: 500 });
  }
}
