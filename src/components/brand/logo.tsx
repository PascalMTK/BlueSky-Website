import Link from "next/link";
import { LogoMark } from "@/components/brand/logo-mark";

export function Logo({ className }: { className?: string }) {
  return (
    <Link
      href="/"
      className={`inline-flex items-center gap-2.5 ${className ?? ""}`}
    >
      <LogoMark size={38} />
      <span className="flex flex-col leading-none">
        <span className="text-lg font-extrabold tracking-tight">
          Blue<span className="text-brand-gold">Sky</span>
        </span>
        <span className="text-[10px] font-semibold uppercase tracking-[0.2em] text-text-muted">
          Money Transfer
        </span>
      </span>
    </Link>
  );
}
