type LogoMarkProps = {
  className?: string;
  size?: number;
};

/**
 * Placeholder recreation of the Blue Sky emblem (circular badge, fanned
 * bill/card motif, "S" accent). Swap for the real exported logo asset in
 * public/images/logo.svg when available.
 */
export function LogoMark({ className, size = 40 }: LogoMarkProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      role="img"
      aria-label="Blue Sky"
    >
      <circle cx="20" cy="20" r="20" fill="var(--color-brand-blue)" />
      <g transform="translate(11 9) rotate(-12 9 11)">
        <rect x="0" y="4" width="14" height="18" rx="2.4" fill="white" fillOpacity="0.28" />
      </g>
      <g transform="translate(13 8) rotate(-4 9 11)">
        <rect x="0" y="4" width="14" height="18" rx="2.4" fill="white" fillOpacity="0.55" />
      </g>
      <g transform="translate(15 7) rotate(6 9 11)">
        <rect x="0" y="4" width="14" height="18" rx="2.4" fill="white" />
        <circle cx="7" cy="13" r="3.1" fill="var(--color-brand-blue)" />
      </g>
      <circle cx="10.5" cy="29.5" r="6" fill="var(--color-brand-gold)" />
      <text
        x="10.5"
        y="33"
        textAnchor="middle"
        fontSize="7.5"
        fontWeight="700"
        fill="var(--color-brand-blue-deep)"
        fontFamily="system-ui, sans-serif"
      >
        S
      </text>
    </svg>
  );
}
