import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Carry Radar — živi funding monitor",
  description:
    "Delta-neutralni funding carry: žive stope po burzama (Binance, Bybit, Hyperliquid), knjiga bota i paper-trading P&L.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="hr">
      <body>{children}</body>
    </html>
  );
}
