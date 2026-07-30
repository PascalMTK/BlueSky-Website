import type { Metadata } from "next";
import { ThemeProvider } from "@/components/theme/theme-provider";
import { ThemeScript } from "@/components/theme/theme-script";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Blue Sky — Transfert d'argent international",
    template: "%s | Blue Sky",
  },
  description:
    "Blue Sky connecte la RDC, la Zambie, la Namibie, l'Afrique du Sud, le Zimbabwe, le Kenya, la Tanzanie et le Malawi pour des transferts d'argent rapides, fiables et sécurisés.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="fr"
      data-scroll-behavior="smooth"
      className="h-full antialiased"
      suppressHydrationWarning
    >
      <head>
        <ThemeScript />
      </head>
      <body className="min-h-full flex flex-col bg-bg text-text">
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
