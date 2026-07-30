export function Kicker({
  children,
  tone = "gold",
}: {
  children: React.ReactNode;
  tone?: "gold" | "blue";
}) {
  const toneClasses =
    tone === "gold"
      ? "text-brand-gold"
      : "text-brand-blue dark:text-brand-cyan";

  return (
    <span
      className={`eyebrow-line inline-flex items-center gap-3 text-[11px] font-bold uppercase tracking-[0.22em] ${toneClasses}`}
    >
      {children}
    </span>
  );
}

export function VerticalRules({ count = 3, className = "" }: { count?: number; className?: string }) {
  return (
    <span className={`brand-rules ${className}`} aria-hidden="true">
      {Array.from({ length: count }).map((_, i) => (
        <span key={i} />
      ))}
    </span>
  );
}
