"use client";

import { useEffect, useMemo, useState } from "react";

type Coin = {
  c: string;
  price: number | null;
  chg24h: number | null;
  spark: number[];
  funding: Record<string, number>;
  bestVenue: string | null;
  bestApy: number | null;
};
type Live = { t: number; venuesOk: Record<string, boolean>; coins: Coin[] };
type Paper = {
  state: {
    initial: number;
    equity: number;
    start_ms: number;
    book: Record<string, string>;
    book_apys: Record<string, number>;
    cum_funding: number;
    cum_coll: number;
    cum_cost: number;
  };
  history: { t: string; equity: number }[];
};

const VENUE_LABEL: Record<string, string> = { binance: "Binance", bybit: "Bybit", hyperliquid: "Hyperliquid" };

function fmtPrice(p: number | null): string {
  if (p == null) return "—";
  if (p >= 1000) return p.toLocaleString("en-US", { maximumFractionDigits: 0 });
  if (p >= 10) return p.toFixed(2);
  if (p >= 0.1) return p.toFixed(4);
  return p.toFixed(6);
}

function Spark({ data }: { data: number[] }) {
  if (!data || data.length < 2) return <span className="mut">—</span>;
  const w = 120, h = 34, pad = 2;
  const min = Math.min(...data), max = Math.max(...data);
  const rng = max - min || 1;
  const pts = data
    .map((v, i) => `${pad + (i * (w - 2 * pad)) / (data.length - 1)},${h - pad - ((v - min) / rng) * (h - 2 * pad)}`)
    .join(" ");
  const up = data[data.length - 1] >= data[0];
  return (
    <svg width={w} height={h} aria-hidden="true">
      <polyline points={pts} fill="none" stroke={up ? "#22c55e" : "#ef4444"} strokeWidth="1.6" />
    </svg>
  );
}

function EquityChart({ history, initial }: { history: { t: string; equity: number }[]; initial: number }) {
  if (!history || history.length < 2) return null;
  const w = 900, h = 190, padX = 6, padY = 12;
  const vals = history.map((r) => r.equity);
  const min = Math.min(...vals, initial), max = Math.max(...vals, initial);
  const rng = max - min || 1;
  const x = (i: number) => padX + (i * (w - 2 * padX)) / (history.length - 1);
  const y = (v: number) => h - padY - ((v - min) / rng) * (h - 2 * padY);
  const line = vals.map((v, i) => `${x(i)},${y(v)}`).join(" ");
  const area = `${padX},${h - padY} ${line} ${w - padX},${h - padY}`;
  return (
    <svg viewBox={`0 0 ${w} ${h}`} style={{ width: "100%", height: "auto" }} role="img" aria-label="Krivulja kapitala paper bota">
      <polygon points={area} fill="rgba(34,197,94,0.08)" />
      <line x1={padX} x2={w - padX} y1={y(initial)} y2={y(initial)} stroke="#8b93a7" strokeWidth="1" strokeDasharray="5 4" />
      <text x={w - padX - 4} y={y(initial) - 5} textAnchor="end" fontSize="11" fill="#8b93a7">
        start ${initial.toFixed(0)}
      </text>
      <polyline points={line} fill="none" stroke="#22c55e" strokeWidth="2" />
      <circle cx={x(vals.length - 1)} cy={y(vals[vals.length - 1])} r="3.5" fill="#22c55e" />
    </svg>
  );
}

export default function Home() {
  const [live, setLive] = useState<Live | null>(null);
  const [paper, setPaper] = useState<Paper | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [ago, setAgo] = useState(0);

  useEffect(() => {
    let alive = true;
    const loadLive = () =>
      fetch("/api/live")
        .then((r) => r.json())
        .then((d) => { if (alive) { setLive(d); setAgo(0); } })
        .catch(() => alive && setErr("Ne mogu dohvatiti žive podatke."));
    const loadPaper = () =>
      fetch("/api/paper")
        .then((r) => r.json())
        .then((d) => alive && !d.error && setPaper(d))
        .catch(() => {});
    loadLive();
    loadPaper();
    const iv = setInterval(loadLive, 60_000);
    const tick = setInterval(() => setAgo((a) => a + 1), 1_000);
    return () => { alive = false; clearInterval(iv); clearInterval(tick); };
  }, []);

  const days = paper ? (Date.now() - paper.state.start_ms) / 86_400_000 : 0;
  const ret = paper ? (paper.state.equity / paper.state.initial - 1) * 100 : 0;
  const book = paper?.state.book ?? {};
  const bookApy = useMemo(() => {
    if (!live) return null;
    const held = Object.entries(book);
    if (!held.length) return null;
    let s = 0, n = 0;
    for (const [c, v] of held) {
      const coin = live.coins.find((x) => x.c === c);
      const f = coin?.funding?.[v];
      if (f != null) { s += f; n++; }
    }
    return n ? s / n : null;
  }, [live, book]);

  return (
    <main className="wrap">
      <div className="header">
        <h1>Carry Radar</h1>
        <div className="livewrap">
          <span className="dot" />
          <span>uživo · osvježeno prije {ago}s</span>
        </div>
      </div>
      <p className="sub">
        Delta-neutralni funding carry — koliko te tržište <i>plaća da čekaš</i>, po burzama. Bez predikcija cijene.
      </p>

      {err && !live && <p className="err">{err}</p>}

      <section className="panel">
        <h2>
          Paper bot <span>· ${paper ? paper.state.initial.toFixed(0) : "1000"} start · rebalans mjesečno · read-only</span>
        </h2>
        {paper ? (
          <>
            <div className="cards">
              <div className="card"><div className="k">Kapital</div><div className="v">${paper.state.equity.toFixed(2)}</div></div>
              <div className="card"><div className="k">Od početka</div><div className="v" style={{ color: ret >= 0 ? "#22c55e" : "#ef4444" }}>{ret >= 0 ? "+" : ""}{ret.toFixed(2)}%</div></div>
              <div className="card"><div className="k">Funding</div><div className="v">${paper.state.cum_funding.toFixed(2)}</div></div>
              <div className="card"><div className="k">Kolateral</div><div className="v">${paper.state.cum_coll.toFixed(2)}</div></div>
              <div className="card"><div className="k">Troškovi</div><div className="v">-${paper.state.cum_cost.toFixed(2)}</div></div>
              <div className="card"><div className="k">Radi</div><div className="v">{days.toFixed(0)} d</div></div>
            </div>
            <EquityChart history={paper.history} initial={paper.state.initial} />
            <div style={{ marginTop: 12 }}>
              <div className="chips">
                {Object.entries(book).map(([c, v]) => (
                  <span key={c} className="chip">
                    {c} <b>@ {VENUE_LABEL[v] ?? v}</b>
                  </span>
                ))}
                {bookApy != null && (
                  <span className="chip">knjiga sad plaća ≈ <b>{bookApy.toFixed(1)}% APY</b></span>
                )}
              </div>
            </div>
          </>
        ) : (
          <p className="mut">Učitavam P&L bota…</p>
        )}
      </section>

      <section className="panel">
        <h2>
          Živi funding po burzama <span>· godišnje (APY) · pozitivno = short-perp strana naplaćuje</span>
        </h2>
        {live ? (
          <div className="tablewrap">
            <table>
              <thead>
                <tr>
                  <th>Coin</th>
                  <th style={{ textAlign: "right" }}>Cijena</th>
                  <th style={{ textAlign: "right" }}>24 h</th>
                  <th>7 dana</th>
                  <th style={{ textAlign: "right" }}>Binance</th>
                  <th style={{ textAlign: "right" }}>Bybit</th>
                  <th style={{ textAlign: "right" }}>Hyperliquid</th>
                  <th>Najbolja</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {live.coins.map((x) => {
                  const held = book[x.c];
                  return (
                    <tr key={x.c}>
                      <td className="sym">{x.c}</td>
                      <td style={{ textAlign: "right" }} className="mut">${fmtPrice(x.price)}</td>
                      <td style={{ textAlign: "right" }} className={x.chg24h == null ? "mut" : x.chg24h >= 0 ? "pos" : "neg"}>
                        {x.chg24h == null ? "—" : `${x.chg24h >= 0 ? "+" : ""}${x.chg24h.toFixed(1)}%`}
                      </td>
                      <td><Spark data={x.spark} /></td>
                      {(["binance", "bybit", "hyperliquid"] as const).map((v) => {
                        const f = x.funding[v];
                        return (
                          <td key={v} style={{ textAlign: "right" }}>
                            <span className={`fchip ${f == null ? "mut" : f >= 0 ? "pos" : "neg"}`}>
                              {f == null ? "—" : `${f >= 0 ? "+" : ""}${f.toFixed(1)}%`}
                            </span>
                          </td>
                        );
                      })}
                      <td>{x.bestVenue ? <span className="best">{VENUE_LABEL[x.bestVenue]}</span> : <span className="mut">—</span>}</td>
                      <td>{held ? <span className="inbook">u knjizi</span> : null}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="mut">Učitavam žive stope…</p>
        )}
      </section>

      <div className="note">
        <b>Zašto ovdje nema "vjerojatnosti rasta"?</b> Testirali smo ML-predikciju smjera pošteno (out-of-sample): nema
        stvarnog edgea — prikazivati takvu vjerojatnost bilo bi izmišljanje. Funding je suprotno: <b>poznat unaprijed</b> i
        stvarno se isplaćuje svakih 1–8 h. Ovo je monitor, ne savjet za ulaganje; paper bot ne šalje naloge.
      </div>

      <p className="foot">
        Izvori uživo: Binance USD-M · Bybit · Hyperliquid — osvježava se svakih 60 s. P&L bota ažurira se jednom dnevno.
      </p>
    </main>
  );
}
