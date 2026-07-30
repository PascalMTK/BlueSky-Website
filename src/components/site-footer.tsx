import Link from "next/link";
import { Mail, Phone, MapPin } from "lucide-react";
import { Container } from "@/components/ui/container";
import { Logo } from "@/components/brand/logo";
import { FacebookIcon, TiktokIcon } from "@/components/icons/social-icons";
import { SITE } from "@/lib/data/site";
import { COUNTRIES } from "@/lib/data/countries";

const QUICK_LINKS = [
  { href: "/a-propos", label: "À propos" },
  { href: "/equipe", label: "Notre équipe" },
  { href: "/impact", label: "Notre impact" },
  { href: "/pays", label: "Nos agences" },
  { href: "/contact", label: "Contact" },
];

export function SiteFooter() {
  const year = new Date().getFullYear();

  return (
    <footer className="subtle-grid bg-brand-blue-deep text-white">
      <Container className="grid gap-12 py-20 md:grid-cols-[1.3fr_1fr_1.2fr]">
        <div className="space-y-5">
          <Logo className="[&_span:last-child]:text-white/60" />
          <p className="max-w-sm text-sm leading-relaxed text-white/70">
            {SITE.mission}
          </p>
          <div className="flex gap-3">
            <a
              href={SITE.social.facebook}
              target="_blank"
              rel="noreferrer noopener"
              aria-label="Facebook"
              className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/10 transition hover:bg-brand-gold hover:text-brand-blue-deep"
            >
              <FacebookIcon />
            </a>
            <a
              href={SITE.social.tiktok}
              target="_blank"
              rel="noreferrer noopener"
              aria-label="TikTok"
              className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/10 transition hover:bg-brand-gold hover:text-brand-blue-deep"
            >
              <TiktokIcon />
            </a>
          </div>
        </div>

        <div>
          <h3 className="mb-5 text-xs font-bold uppercase tracking-[.2em] text-brand-gold">
            Navigation
          </h3>
          <ul className="space-y-2.5 text-sm text-white/75">
            {QUICK_LINKS.map((link) => (
              <li key={link.href}>
                <Link href={link.href} className="transition hover:text-white">
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="mb-5 text-xs font-bold uppercase tracking-[.2em] text-brand-gold">
            Contact direct
          </h3>
          <ul className="space-y-3 text-sm text-white/75">
            <li className="flex items-start gap-2.5">
              <MapPin size={16} className="mt-0.5 shrink-0 text-brand-gold" />
              <span>{SITE.headOfficeAddress}</span>
            </li>
            <li className="flex items-center gap-2.5">
              <Phone size={16} className="shrink-0 text-brand-gold" />
              <span>{SITE.primaryPhone}</span>
            </li>
            <li className="flex items-center gap-2.5">
              <Mail size={16} className="shrink-0 text-brand-gold" />
              <span>{SITE.primaryEmail}</span>
            </li>
          </ul>
        </div>
      </Container>

      <div className="border-t border-white/10">
        <Container className="flex flex-col gap-2 py-6 text-xs text-white/50 sm:flex-row sm:items-center sm:justify-between">
          <p>
            © {year} Blue Sky Money Transfer. Tous droits réservés.
          </p>
          <p className="flex flex-wrap gap-x-2">
            Présent dans {COUNTRIES.length} pays :{" "}
            {COUNTRIES.map((c) => c.name).join(" · ")}
          </p>
        </Container>
      </div>
    </footer>
  );
}
