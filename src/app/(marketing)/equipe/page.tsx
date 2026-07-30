import type { Metadata } from "next";
import Image from "next/image";
import { Handshake, Ear, Rocket, HeartHandshake } from "lucide-react";
import { Container } from "@/components/ui/container";
import { Kicker } from "@/components/ui/kicker";
import { COUNTRIES } from "@/lib/data/countries";

export const metadata: Metadata = {
  title: "Notre équipe",
  description:
    "Rencontrez l'équipe Blue Sky, présente sur le terrain dans chacun de nos pays pour accompagner vos transferts d'argent.",
};

const VALUES = [
  {
    icon: Handshake,
    title: "Proximité",
    text: "Des agents présents physiquement dans chaque pays, pas seulement une application.",
  },
  {
    icon: Ear,
    title: "Écoute",
    text: "Chaque client a une situation différente ; notre équipe prend le temps de comprendre.",
  },
  {
    icon: Rocket,
    title: "Réactivité",
    text: "Des réponses rapides sur WhatsApp et par téléphone, y compris en dehors des heures classiques.",
  },
  {
    icon: HeartHandshake,
    title: "Engagement",
    text: "Une équipe impliquée dans les communautés qu'elle sert, au-delà des transactions.",
  },
];

export default function TeamPage() {
  return (
    <>
      <section className="bg-brand-blue py-16 text-white sm:py-20">
        <Container className="text-center">
          <Kicker>L&apos;équipe Blue Sky</Kicker>
          <h1 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold sm:text-5xl">
            Des visages, pas seulement une plateforme
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-white/70">
            Derrière chaque transfert Blue Sky, une équipe basée en Afrique
            australe travaille chaque jour pour que votre argent arrive vite
            et en sécurité.
          </p>
        </Container>
      </section>

      <section className="py-20 sm:py-28">
        <Container>
          <div className="overflow-hidden rounded-[2rem] shadow-2xl">
            <Image
              src="/images/team-photo.jpg"
              alt="L'équipe Blue Sky réunie sur le terrain"
              width={1600}
              height={900}
              className="h-[320px] w-full object-cover sm:h-[480px]"
              priority
            />
          </div>
          <p className="mx-auto mt-8 max-w-3xl text-center leading-relaxed text-text-muted">
            Notre équipe combine des profils opérationnels, un service client
            réactif et des agents locaux répartis dans nos {COUNTRIES.length}{" "}
            pays de couverture — de Lubumbashi à Windhoek, en passant par
            Lusaka et Lilongwe.
          </p>
        </Container>
      </section>

      <section className="bg-surface-muted py-20 sm:py-28">
        <Container>
          <div className="mx-auto mb-14 max-w-2xl text-center">
            <Kicker tone="blue">Ce qui nous anime</Kicker>
            <h2 className="mt-4 text-3xl font-extrabold sm:text-4xl">
              Les valeurs qui guident notre équipe
            </h2>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {VALUES.map(({ icon: Icon, title, text }) => (
              <div key={title} className="rounded-2xl bg-surface p-7 shadow-sm">
                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-brand-gold text-brand-blue-deep">
                  <Icon size={22} />
                </div>
                <h3 className="mb-2 text-lg font-bold">{title}</h3>
                <p className="text-sm leading-relaxed text-text-muted">{text}</p>
              </div>
            ))}
          </div>
        </Container>
      </section>
    </>
  );
}
