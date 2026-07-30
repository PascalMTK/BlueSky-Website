"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Users, SendHorizonal } from "lucide-react";

const NAV_ITEMS = [
  { href: "/tableau-de-bord", label: "Vue d'ensemble", icon: LayoutDashboard, exact: true },
  { href: "/tableau-de-bord/beneficiaires", label: "Bénéficiaires", icon: Users },
  { href: "/tableau-de-bord/nouveau-transfert", label: "Nouveau transfert", icon: SendHorizonal },
];

export function DashboardNav({ className = "space-y-1" }: { className?: string }) {
  const pathname = usePathname();

  return (
    <nav className={className}>
      {NAV_ITEMS.map(({ href, label, icon: Icon, exact }) => {
        const active = exact ? pathname === href : pathname.startsWith(href);
        return (
          <Link
            key={href}
            href={href}
            className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition ${
              active
                ? "bg-brand-blue text-white"
                : "text-text-muted hover:bg-surface-muted hover:text-text lg:text-white/60 lg:hover:bg-white/10 lg:hover:text-white"
            }`}
          >
            <Icon size={18} />
            {label}
          </Link>
        );
      })}
    </nav>
  );
}
