import type { Metadata } from "next";
import Image from "next/image";
import { HandHeart, ArrowRight } from "lucide-react";
import { Container } from "@/components/ui/container";
import { Kicker } from "@/components/ui/kicker";
import { LinkButton } from "@/components/ui/button";

export const metadata: Metadata = {
  title: "Notre impact",
  description:
    "Blue Sky s'engage auprès des communautés qu'elle sert, notamment à travers des visites régulières à un orphelinat en Namibie.",
};

export default function ImpactPage() {
  return (
    <>
      <section className="bg-brand-blue py-16 text-white sm:py-20">
        <Container className="text-center">
          <Kicker>Responsabilité sociale</Kicker>
          <h1 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold sm:text-5xl">
            Connecter les familles, soutenir les communautés
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-white/70">
            Le métier de Blue Sky est de rapprocher les familles séparées par
            la distance. Nous croyons que cette mission ne s&apos;arrête pas
            à la transaction.
          </p>
        </Container>
      </section>

      <section className="py-20 sm:py-28">
        <Container className="grid items-center gap-14 lg:grid-cols-2">
          <div className="space-y-6">
            <div className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-brand-gold text-brand-blue-deep">
              <HandHeart size={22} />
            </div>
            <h2 className="text-3xl font-extrabold sm:text-4xl">
              Aux côtés d&apos;un orphelinat en Namibie
            </h2>
            <p className="leading-relaxed text-text-muted">
              L&apos;équipe Blue Sky se déplace régulièrement auprès
              d&apos;enfants d&apos;un orphelinat en Namibie pour partager du
              temps, apporter des ressources et rester à l&apos;écoute de
              leurs besoins. Ces visites font partie de l&apos;identité de
              Blue Sky : une entreprise africaine, construite par et pour ses
              communautés.
            </p>
            <p className="leading-relaxed text-text-muted">
              Une partie de notre présence locale dans chaque pays sert aussi
              à identifier des initiatives communautaires que nous pouvons
              soutenir, ponctuellement ou dans la durée.
            </p>
          </div>
          <div className="overflow-hidden rounded-[2rem] shadow-2xl">
            <Image
              src="/images/community-outreach-portrait.jpg"
              alt="Une membre de l'équipe Blue Sky avec une enfant de l'orphelinat"
              width={800}
              height={1000}
              className="h-[420px] w-full object-cover sm:h-[520px]"
              priority
            />
          </div>
        </Container>
      </section>

      <section className="bg-surface-muted py-20 sm:py-28">
        <Container>
          <div className="overflow-hidden rounded-[2rem] shadow-2xl">
            <Image
              src="/images/community-outreach-group.jpg"
              alt="L'équipe Blue Sky entourée des enfants de l'orphelinat lors d'une visite"
              width={1600}
              height={1000}
              className="h-[340px] w-full object-cover sm:h-[500px]"
            />
          </div>
          <div className="mx-auto mt-10 max-w-2xl text-center">
            <h2 className="text-2xl font-extrabold sm:text-3xl">
              Vous connaissez une initiative locale à soutenir ?
            </h2>
            <p className="mt-3 text-text-muted">
              Parlez-nous de votre communauté — nous sommes toujours à
              l&apos;écoute de nouvelles façons de nous rendre utiles là où
              nous opérons.
            </p>
            <div className="mt-6">
              <LinkButton href="/contact" variant="secondary">
                Nous écrire <ArrowRight size={16} />
              </LinkButton>
            </div>
          </div>
        </Container>
      </section>
    </>
  );
}
