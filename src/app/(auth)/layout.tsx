import Image from "next/image";
import { Logo } from "@/components/brand/logo";
import { VerticalRules } from "@/components/ui/kicker";
import { ThemeToggle } from "@/components/theme/theme-toggle";
import { COUNTRIES } from "@/lib/data/countries";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      <div className="relative hidden overflow-hidden bg-brand-blue-deep text-white lg:flex lg:flex-col lg:justify-between lg:p-12">
        <Image
          src="/images/team-photo.jpg"
          alt=""
          fill
          sizes="50vw"
          className="object-cover opacity-20"
          priority
        />
        <div className="relative z-10">
          <Logo className="[&_span]:text-white" />
        </div>
        <div className="relative z-10 space-y-6">
          <div className="flex items-center gap-3 text-white/70">
            <VerticalRules />
            <p className="max-w-sm text-lg font-medium leading-snug">
              Construisez votre avenir en toute sécurité et en toute
              confiance avec Blue Sky.
            </p>
          </div>
          <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm text-white/50">
            {COUNTRIES.map((c) => (
              <span key={c.code}>
                {c.flag} {c.name}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="relative flex flex-col justify-center p-6 sm:p-12">
        <div className="absolute right-6 top-6">
          <ThemeToggle />
        </div>
        <div className="mx-auto w-full max-w-md">
          <div className="mb-8 lg:hidden">
            <Logo />
          </div>
          {children}
        </div>
      </div>
    </div>
  );
}
