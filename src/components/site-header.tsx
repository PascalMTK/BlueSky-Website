"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Menu, X, ArrowUpRight } from "lucide-react";
import { Container } from "@/components/ui/container";
import { Logo } from "@/components/brand/logo";
import { LinkButton } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme/theme-toggle";

const NAV_ITEMS = [
  { href: "/", label: "Accueil" },
  { href: "/a-propos", label: "À propos" },
  { href: "/equipe", label: "Équipe" },
  { href: "/impact", label: "Impact" },
  { href: "/pays", label: "Nos pays" },
  { href: "/contact", label: "Contact" },
];

export function SiteHeader({ userName }: { userName: string | null }) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-border/70 bg-surface/90 shadow-[0_18px_40px_-32px_rgba(5,26,56,.6)] backdrop-blur-xl">
      <Container className="flex h-[72px] items-center justify-between">
        <div className="transition-transform duration-300 hover:-translate-y-0.5">
          <Logo />
        </div>

        <nav className="hidden lg:flex items-center gap-0.5 text-[13px] font-semibold">
          {NAV_ITEMS.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`relative rounded-lg px-3 py-2 transition-all hover:-translate-y-0.5 hover:bg-surface-muted hover:text-brand-blue dark:hover:text-brand-gold-light ${
                  active ? "bg-surface-muted text-brand-blue dark:text-brand-gold-light" : "text-text-muted"
                }`}
              >
                {item.label}
                {active && (
                  <span className="absolute inset-x-3 -bottom-[1px] h-[2px] rounded-full bg-brand-blue shadow-[0_0_10px_2px_rgba(8,87,201,.5)] dark:bg-brand-gold-light dark:shadow-[0_0_10px_2px_rgba(255,217,133,.5)]" />
                )}
              </Link>
            );
          })}
        </nav>

        <div className="hidden lg:flex items-center gap-3">
          <ThemeToggle />
          {userName ? (
            <LinkButton href="/tableau-de-bord" variant="secondary">
              Tableau de bord
            </LinkButton>
          ) : (
            <>
              <LinkButton href="/connexion" variant="ghost">
                Connexion
              </LinkButton>
              <LinkButton href="/inscription" variant="primary">
                Ouvrir un compte <ArrowUpRight size={15} />
              </LinkButton>
            </>
          )}
        </div>

        <div className="flex items-center gap-2 lg:hidden">
          <ThemeToggle />
          <button
            type="button"
            aria-label="Menu"
            onClick={() => setOpen((v) => !v)}
            className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-border"
          >
            {open ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </Container>

      {open && (
        <div className="border-t border-border bg-surface lg:hidden">
          <Container className="flex flex-col gap-1 py-4">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-2.5 text-sm font-semibold text-text hover:bg-surface-muted"
              >
                {item.label}
              </Link>
            ))}
            <div className="mt-3 flex flex-col gap-2">
              {userName ? (
                <LinkButton href="/tableau-de-bord" variant="secondary">
                  Tableau de bord
                </LinkButton>
              ) : (
                <>
                  <LinkButton href="/connexion" variant="ghost">
                    Connexion
                  </LinkButton>
                  <LinkButton href="/inscription" variant="primary">
                    Ouvrir un compte
                  </LinkButton>
                </>
              )}
            </div>
          </Container>
        </div>
      )}
    </header>
  );
}
