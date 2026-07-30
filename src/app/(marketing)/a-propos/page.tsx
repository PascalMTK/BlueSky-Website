import type { Metadata } from "next";
import Image from "next/image";
import { Target, Compass, Quote } from "lucide-react";
import { Container } from "@/components/ui/container";
import { Kicker } from "@/components/ui/kicker";
import { LinkButton } from "@/components/ui/button";
import { SITE } from "@/lib/data/site";

export const metadata: Metadata = {
  title: "À propos",
  description:
    "Découvrez la mission, la vision et l'histoire de Blue Sky, agence de transfert d'argent au service de l'Afrique australe et de l'Est.",
};

export default function AboutPage() {
  return (
    <>
      <section className="bg-brand-blue py-16 text-white sm:py-20">
        <Container className="text-center">
          <Kicker>Qui sommes-nous ?</Kicker>
          <h1 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold sm:text-5xl">
            Une agence bâtie pour rapprocher les familles africaines
          </h1>
        </Container>
      </section>

      <section className="py-20 sm:py-28">
        <Container className="grid items-center gap-14 lg:grid-cols-2">
          <p className="text-lg leading-relaxed text-text-muted">
            {SITE.definition}
          </p>
          <div className="grid gap-6 sm:grid-cols-2">
            <div className="rounded-2xl border border-border bg-surface p-7">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-brand-gold text-brand-blue-deep">
                <Target size={22} />
              </div>
              <h3 className="mb-2 text-lg font-bold">Notre but</h3>
              <p className="text-sm leading-relaxed text-text-muted">
                {SITE.purpose}
              </p>
            </div>
            <div className="rounded-2xl border border-border bg-surface p-7">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-brand-blue/10 text-brand-blue dark:bg-white/10 dark:text-brand-gold-light">
                <Compass size={22} />
              </div>
              <h3 className="mb-2 text-lg font-bold">Notre mission</h3>
              <p className="text-sm leading-relaxed text-text-muted">
                {SITE.mission}
              </p>
            </div>
          </div>
        </Container>
      </section>

      {/* Vision, paired with the founder portrait */}
      <section className="bg-surface-muted py-20 sm:py-28">
        <Container className="grid items-center gap-14 lg:grid-cols-[0.85fr_1.15fr]">
          <div className="relative mx-auto w-full max-w-sm">
            <div className="absolute -inset-4 -z-10 rounded-[2.5rem] bg-brand-blue/10" />
            <div className="overflow-hidden rounded-[2rem] shadow-2xl">
              <Image
                src="/images/founder-portrait.jpg"
                alt="Fondatrice de Blue Sky"
                width={700}
                height={900}
                className="h-[480px] w-full object-cover object-top"
                priority
              />
            </div>
          </div>
          <div className="space-y-6">
            <Kicker tone="blue">Notre vision</Kicker>
            <Quote className="text-brand-gold" size={36} />
            <p className="text-2xl font-semibold leading-snug sm:text-3xl">
              &laquo; Nous voulons qu&apos;aucune distance, aucune frontière
              n&apos;empêche une famille de prendre soin des siens. Blue Sky
              existe pour que chaque franc, chaque kwacha, chaque rand envoyé
              arrive à destination avec la même confiance qu&apos;une
              remise en main propre. &raquo;
            </p>
            <p className="text-sm text-text-muted">
              L&apos;équipe de direction, Blue Sky
            </p>
            <p className="leading-relaxed text-text-muted">
              Cette vision guide chacune de nos décisions : ouvrir de
              nouvelles agences là où les familles en ont besoin, simplifier
              chaque étape du transfert, et rester joignables humainement,
              pas seulement via une application.
            </p>
            <LinkButton href="/inscription" variant="secondary">
              Rejoindre Blue Sky
            </LinkButton>
          </div>
        </Container>
      </section>
    </>
  );
}
