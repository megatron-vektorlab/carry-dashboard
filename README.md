# Carry Radar

Živi web-monitor za delta-neutralni funding carry.

- **/api/live** — žive funding stope (Binance USD-M, Bybit, Hyperliquid), cijene, 24h promjena i 7-dnevni sparkline po coinu. Server-side fetch (regija `fra1` zbog geo-ograničenja burzi), bez API ključeva — sve javni endpointi.
- **/api/paper** — stanje i povijest paper-trading carry bota (datoteke u `data/`, sinkronizira ih dnevni Windows task iz `binance app/engine/carry/`).
- **/** — dashboard: knjiga bota, P&L krivulja, tablica funding APY-a po burzama s najboljom burzom po coinu.

Bez predikcija cijene — prikazuje se samo funding koji se stvarno isplaćuje (poznat unaprijed) i činjenično kretanje cijena.

## Dev

```bash
npm install
npm run dev
```

## Deploy

Vercel (GitHub auto-deploy). `vercel.json` postavlja regiju funkcija na `fra1` — obavezno, jer Binance/Bybit blokiraju US IP-ove.

Podaci bota: dnevni scheduled task (`CryptoRotCarryPaper`) kopira `paper_state.json` + `paper_history.csv` u `data/` i push-a — Vercel se sam redeploya.
