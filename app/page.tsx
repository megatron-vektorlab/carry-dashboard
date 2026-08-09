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
  ml?: {
    state: { equity: number; initial: number; symbol: string; trades: number; fees: number; started_at: string };
    history: { t: string; equity: number }[];
  } | null;
};

function parseUtc(t: string): number {
  return Date.parse(t.replace(" UTC", "Z").replace(" ", "T"));
}

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

function RaceChart({
  carry,
  ml,
  initial,
}: {
  carry: { t: string; equity: number }[];
  ml?: { t: string; equity: number }[] | null;
  initial: number;
}) {
  if (!carry || carry.length < 2) return null;
  const w = 900, h = 190, padX = 6, padY = 12;

  const cPts = carry.map((r) => ({ ms: parseUtc(r.t), v: r.equity })).filter((p) => !Number.isNaN(p.ms));
  const mPts = (ml ?? []).map((r) => ({ ms: parseUtc(r.t), v: r.equity })).filter((p) => !Number.isNaN(p.ms));

  const allV = [...cPts.map((p) => p.v), ...mPts.map((p) => p.v), initial];
  const min = Math.min(...allV), max = Math.max(...allV);
  const rng = max - min || 1;
  const t0 = Math.min(...cPts.map((p) => p.ms), ...(mPts.length ? mPts.map((p) => p.ms) : [Infinity]));
  const t1 = Math.max(...cPts.map((p) => p.ms), ...(mPts.length ? mPts.map((p) => p.ms) : [-Infinity]));
  const tr = t1 - t0 || 1;

  const x = (ms: number) => padX + ((ms - t0) / tr) * (w - 2 * padX);
  const y = (v: number) => h - padY - ((v - min) / rng) * (h - 2 * padY);
  const toLine = (pts: { ms: number; v: number }[]) => pts.map((p) => `${x(p.ms)},${y(p.v)}`).join(" ");

  const cLine = toLine(cPts);
  const area = `${x(cPts[0].ms)},${h - padY} ${cLine} ${x(cPts[cPts.length - 1].ms)},${h - padY}`;

  return (
    <svg viewBox={`0 0 ${w} ${h}`} style={{ width: "100%", height: "auto" }} role="img" aria-label="Utrka kapitala: carry bot i ML eksperiment">
      <polygon points={area} fill="rgba(34,197,94,0.07)" />
      <line x1={padX} x2={w - padX} y1={y(initial)} y2={y(initial)} stroke="#8b93a7" strokeWidth="1" strokeDasharray="5 4" />
      <text x={w - padX - 4} y={y(initial) - 5} textAnchor="end" fontSize="11" fill="#8b93a7">
        start ${initial.toFixed(0)}
      </text>
      <polyline points={cLine} fill="none" stroke="#22c55e" strokeWidth="2" />
      <circle cx={x(cPts[cPts.length - 1].ms)} cy={y(cPts[cPts.length - 1].v)} r="3.5" fill="#22c55e" />
      {mPts.length >= 2 && <polyline points={toLine(mPts)} fill="none" stroke="#f59e0b" strokeWidth="2" />}
      {mPts.length >= 1 && (
        <circle cx={x(mPts[mPts.length - 1].ms)} cy={y(mPts[mPts.length - 1].v)} r="3.5" fill="#f59e0b" />
      )}
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

  // How stale is the bot's P&L file? (updates daily at 08:00)
  const staleDays = useMemo(() => {
    if (!paper?.history?.length) return null;
    const last = paper.history[paper.history.length - 1].t; // "2026-06-23 06:00 UTC"
    const ms = Date.parse(last.replace(" ", "T").replace(" UTC", "Z"));
    return Number.isNaN(ms) ? null : (Date.now() - ms) / 86_400_000;
  }, [paper]);

  const perYear = bookApy != null && paper ? (paper.state.equity * bookApy) / 100 : null;

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
        Nadzorna ploča strategije <b>funding carry</b>: umjesto pogađanja hoće li cijena rasti ili padati, prati se{" "}
        <b>kamata (funding)</b> koju burze isplaćuju svakih 1–8 sati. Zeleno = kamata se naplaćuje. Sve ispod je objašnjeno
        običnim jezikom.
      </p>

      {paper && (
        <div className={`banner ${staleDays != null && staleDays > 2 ? "warn" : ""}`}>
          {staleDays != null && staleDays > 2 ? (
            <>
              <b>⚠ Podaci bota nisu svježi.</b> P&L je zadnji put ažuriran prije {staleDays.toFixed(0)} dana — provjerite
              je li računalo bilo upaljeno u 08:00 (zadatak "CryptoRotCarryPaper").
            </>
          ) : (
            <>
              <b>✓ Sve radi samo od sebe — ne trebate ništa napraviti.</b> Bot je nakon {days.toFixed(0)} dana na{" "}
              <b className={ret >= 0 ? "pos" : "neg"}>{ret >= 0 ? "+" : ""}{ret.toFixed(2)}%</b>
              {bookApy != null && (
                <>
                  , a pozicije koje drži trenutno plaćaju <b>≈ {bookApy.toFixed(1)}% godišnje</b>
                  {perYear != null && <> (≈ ${perYear.toFixed(0)}/god na ovaj ulog)</>}
                </>
              )}
              . Brojke se ažuriraju same: cijene svakih 60 s, P&L botova svako jutro u 08:00.
              {paper.ml && (
                <>
                  {" "}Usporedno trči i <b style={{ color: "#f59e0b" }}>ML eksperiment</b>: $
                  {paper.ml.state.equity.toFixed(2)}.
                </>
              )}
            </>
          )}
        </div>
      )}

      {err && !live && <p className="err">{err}</p>}

      <section className="panel">
        <h2>
          1 · Utrka virtualnih botova <span>· dva pristupa, svaki sa svojih $1000 — ništa od ovoga nije pravi novac</span>
        </h2>
        {paper ? (
          <>
            <div className="cards">
              <div className="card">
                <div className="k">Kapital</div>
                <div className="v">${paper.state.equity.toFixed(2)}</div>
                <div className="d">koliko virtualnih $1000 vrijedi danas</div>
              </div>
              <div className="card">
                <div className="k">Od početka</div>
                <div className="v" style={{ color: ret >= 0 ? "#22c55e" : "#ef4444" }}>{ret >= 0 ? "+" : ""}{ret.toFixed(2)}%</div>
                <div className="d">ukupna promjena od starta (15.6.)</div>
              </div>
              <div className="card">
                <div className="k">Funding</div>
                <div className="v">+${paper.state.cum_funding.toFixed(2)}</div>
                <div className="d">zarađena kamata s burzi</div>
              </div>
              <div className="card">
                <div className="k">Kolateral</div>
                <div className="v">+${paper.state.cum_coll.toFixed(2)}</div>
                <div className="d">kamata na USDC (~4,5% god.)</div>
              </div>
              <div className="card">
                <div className="k">Troškovi</div>
                <div className="v">-${paper.state.cum_cost.toFixed(2)}</div>
                <div className="d">naknade za otvaranje pozicija</div>
              </div>
              <div className="card">
                <div className="k">Radi</div>
                <div className="v">{days.toFixed(0)} d</div>
                <div className="d">automatski, bez nadzora</div>
              </div>
            </div>
            <p className="legend" style={{ marginTop: 10 }}>
              <span style={{ color: "#22c55e" }}>━ Carry bot</span> (kamata, delta-neutralno) ·{" "}
              <span style={{ color: "#f59e0b" }}>━ ML rotacija</span> (predviđanje vjerojatnosti — eksperiment)
            </p>
            <RaceChart carry={paper.history} ml={paper.ml?.history} initial={paper.state.initial} />
            {paper.ml && (
              <div className="mlstrip">
                <b>ML rotacija (eksperiment):</b> ${paper.ml.state.equity.toFixed(2)} (
                {(((paper.ml.state.equity / paper.ml.state.initial) - 1) * 100).toFixed(2)}%) · drži{" "}
                {paper.ml.state.symbol.replace("/USDT", "")} · {paper.ml.state.trades} rotacija
                <span className="mut">
                  {" "}— isti model vjerojatnosti kao izvorni CryptoRot (68 featurea, svjež trening svakih 30 dana).
                  Pošteni test je predvidio da će izgubiti od carryja — ovdje se uživo vidi hoćemo li imati sreće.
                </span>
              </div>
            )}
            <div style={{ marginTop: 12 }}>
              <div className="chips">
                {Object.entries(book).map(([c, v]) => (
                  <span key={c} className="chip">
                    {c} <b>@ {VENUE_LABEL[v] ?? v}</b>
                  </span>
                ))}
                {bookApy != null && (
                  <span className="chip">
                    ove pozicije sad plaćaju ≈ <b>{bookApy.toFixed(1)}% god.</b>
                  </span>
                )}
              </div>
            </div>
            <details>
              <summary>Kako čitati ovaj dio?</summary>
              <ul>
                <li><b>Zelena linija</b> = carry bot (skuplja kamatu, zaštićen od pada cijena). <b>Narančasta linija</b> = ML eksperiment koji pokušava predvidjeti koje valute će rasti — kreće kasnije, pa mu je linija kraća. Isprekidana crta = početnih $1000 za oba.</li>
                <li><b>Zašto utrka?</b> Pošten test na prošlosti kaže da predviđanje gubi od kamate. Umjesto da vjerujemo testu na riječ, pustili smo oba pristupa da se natječu uživo — pobjednika će pokazati graf, ne mišljenje.</li>
                <li><b>Pločice ispod grafa</b> = što bot trenutno "drži" i na kojoj burzi naplaćuje kamatu (npr. "BTC @ Hyperliquid").</li>
                <li>Zarada dolazi iz dva izvora: <b>funding</b> (kamata s burze) i <b>kolateral</b> (kamata na dolare). Troškovi se plaćaju samo pri izmjeni pozicija — zato bot mijenja pozicije najviše jednom mjesečno.</li>
                <li>Bot je <b>delta-neutralan</b>: zaštićen je od pada cijene, pa i kad kripto padne, ova linija ne bi trebala padati s njim.</li>
              </ul>
            </details>
          </>
        ) : (
          <p className="mut">Učitavam P&L bota…</p>
        )}
      </section>

      <section className="panel">
        <h2>
          2 · Kamate uživo po burzama <span>· koje valute trenutno najviše plaćaju i gdje</span>
        </h2>
        <p className="legend">
          <span className="pos">■ zeleno</span> = burza <b>plaća</b> onome tko drži zaštićenu (short-perp) poziciju ·{" "}
          <span className="neg">■ crveno</span> = ta strana <b>plaća</b> burzi (izbjegava se) ·{" "}
          <span className="inbook">u knjizi</span> = bot to trenutno drži · brojke su godišnje (APY)
        </p>
        {live ? (
          <div className="tablewrap">
            <table>
              <thead>
                <tr>
                  <th>Coin</th>
                  <th style={{ textAlign: "right" }}>Cijena</th>
                  <th style={{ textAlign: "right" }} title="Promjena cijene u zadnja 24 sata — samo informativno, bot ne ovisi o njoj">24 h</th>
                  <th title="Kretanje cijene u zadnjih 7 dana">7 dana</th>
                  <th style={{ textAlign: "right" }}>Binance</th>
                  <th style={{ textAlign: "right" }}>Bybit</th>
                  <th style={{ textAlign: "right" }}>Hyperliquid</th>
                  <th title="Burza koja trenutno plaća najveću kamatu za ovaj coin">Najbolja</th>
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
        <details>
          <summary>Kako čitati ovu tablicu?</summary>
          <ul>
            <li><b>Što je funding?</b> Na burzama postoje "perpetual" ugovori. Da bi njihova cijena pratila stvarnu, jedna strana svakih 1–8 h plaća kamatu drugoj. Kad je tržište optimistično, plaćaju oni koji se klade na rast — a naplaćuje <b>zaštićena strana</b>, na kojoj je bot.</li>
            <li><b>Tri stupca s postocima</b> = ista valuta često plaća različito na različitim burzama. Bot uvijek bira stupac s najvećim brojem — to je "Najbolja".</li>
            <li><b>Primjer:</b> +11% kod BTC-a znači: tko drži zaštićenu BTC poziciju od $1000, prima ≈ $110 godišnje — bez obzira raste li BTC ili pada.</li>
            <li><b>Kamate se stalno mijenjaju</b> — zato se tablica osvježava svake minute, a bot pozicije mijenja tek kad se isplati (najviše jednom mjesečno, da ne izgori na troškovima).</li>
            <li>Tablica je poredana od valute koja plaća najviše prema onima koje plaćaju najmanje.</li>
          </ul>
        </details>
      </section>

      <section className="panel">
        <h2>3 · Rječnik <span>· pojmovi na stranici, običnim jezikom</span></h2>
        <div className="gloss">
          <div><b>Funding (kamata)</b><span>naknada koju burza prebacuje između kupaca i prodavatelja svakih 1–8 h; jedini prihod koji je poznat unaprijed</span></div>
          <div><b>Delta-neutralno</b><span>pozicija složena tako da pad ili rast cijene ne mijenja vrijednost — zarađuje se samo kamata</span></div>
          <div><b>Short-perp</b><span>zaštitna strana perpetual ugovora; u optimističnom tržištu ona naplaćuje funding</span></div>
          <div><b>Knjiga</b><span>popis pozicija koje bot trenutno drži (max 6 valuta, jednaki iznosi)</span></div>
          <div><b>APY</b><span>godišnja stopa: +11% APY na $1000 ≈ $110 godišnje ako se stopa zadrži</span></div>
          <div><b>Kolateral</b><span>dolari (USDC) koji stoje iza pozicija; i oni nose kamatu ~4,5% godišnje</span></div>
          <div><b>Rebalans</b><span>mjesečna izmjena knjige: bot prebaci u valute/burze koje tada plaćaju najviše</span></div>
          <div><b>Paper trading</b><span>vježba: sve stope i računice su stvarne, ali se ne šalju nalozi i ne riskira pravi novac</span></div>
        </div>
      </section>

      <div className="note">
        <b>Zašto ovdje nema "vjerojatnosti rasta"?</b> Testirali smo ML-predikciju smjera pošteno (out-of-sample): nema
        stvarnog edgea — prikazivati takvu vjerojatnost bilo bi izmišljanje. Funding je suprotno: <b>poznat unaprijed</b> i
        stvarno se isplaćuje svakih 1–8 h. Ovo je monitor, ne savjet za ulaganje; virtualni bot ne šalje naloge.
      </div>

      <p className="foot">
        Izvori uživo: Binance USD-M · Bybit · Hyperliquid — osvježava se svakih 60 s. P&L bota ažurira se jednom dnevno u 08:00.
      </p>
    </main>
  );
}
