export function BlobDivider({ className = "" }: { className?: string }) {
  return (
    <svg
      aria-hidden="true"
      className={`pointer-events-none absolute inset-x-0 bottom-0 h-16 w-full sm:h-24 ${className}`}
      viewBox="0 0 1440 110"
      preserveAspectRatio="none"
    >
      <path
        d="M0,32 C180,90 340,4 520,36 C700,68 760,10 960,18 C1160,26 1260,80 1440,40 L1440,110 L0,110 Z"
        fill="var(--color-bg)"
      />
    </svg>
  );
}
