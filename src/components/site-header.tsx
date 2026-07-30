"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Menu, X } from "lucide-react";
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
    <header className="sticky top-0 z-50 border-b border-border/70 bg-surface/85 backdrop-blur-xl">
      <Container className="flex h-[76px] items-center justify-between">
        <Logo />

        <nav className="hidden lg:flex items-center gap-1 rounded-full border border-border bg-surface-muted/60 p-1 text-[13px] font-semibold">
          {NAV_ITEMS.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-full px-3.5 py-2 transition-all hover:text-brand-blue dark:hover:text-brand-gold-light ${
                  active ? "bg-surface text-brand-blue shadow-sm dark:text-brand-gold-light" : "text-text-muted"
                }`}
              >
                {item.label}
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
                Ouvrir un compte
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
