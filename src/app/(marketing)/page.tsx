import Image from "next/image";
import {
  ShieldCheck,
  Zap,
  Globe2,
  Headset,
  UserPlus,
  Send,
  CheckCircle2,
  ArrowRight,
  BadgeCheck,
  Clock3,
} from "lucide-react";
import { Container } from "@/components/ui/container";
import { Kicker, VerticalRules } from "@/components/ui/kicker";
import { LinkButton } from "@/components/ui/button";
import { CountryCard } from "@/components/country-card";
import { BlobDivider } from "@/components/ui/blob-divider";
import { COUNTRIES } from "@/lib/data/countries";
import { SITE } from "@/lib/data/site";

const FEATURES = [
  {
    icon: ShieldCheck,
    title: "100% sécurisé",
    text: "Chaque transaction est protégée et suivie de bout en bout, sans mauvaise surprise.",
  },
  {
    icon: Zap,
    title: "Ultra rapide",
    text: "Vos bénéficiaires reçoivent leurs fonds en quelques minutes, pas en quelques jours.",
  },
  {
    icon: Globe2,
    title: "Réseau régional",
    text: `${COUNTRIES.length} pays d'Afrique australe et de l'Est connectés à une seule plateforme.`,
  },
  {
    icon: Headset,
    title: "Assistance humaine",
    text: "Une équipe joignable sur WhatsApp et par téléphone, dans chaque pays où nous opérons.",
  },
];

const STEPS = [
  {
    icon: UserPlus,
    title: "Créez votre compte",
    text: "Inscription en quelques minutes pour accéder à votre tableau de bord Blue Sky.",
  },
  {
    icon: Send,
    title: "Ajoutez un bénéficiaire",
    text: "Enregistrez les informations de la personne qui recevra les fonds.",
  },
  {
    icon: CheckCircle2,
    title: "Envoyez en toute confiance",
    text: "Choisissez le montant et le moyen de paiement, nous nous occupons du reste.",
  },
];

export default function HomePage() {
  return (
    <>
      {/* Hero */}
      <section className="subtle-grid relative overflow-hidden bg-brand-blue-deep text-white">
        <div aria-hidden className="absolute left-[-12rem] top-[-12rem] h-[34rem] w-[34rem] rounded-full bg-brand-blue/35 blur-[100px]" />
        <div aria-hidden className="absolute bottom-[-10rem] right-[-4rem] h-[28rem] w-[28rem] rounded-full bg-brand-cyan/10 blur-[90px]" />
        <Container className="relative grid min-h-[720px] gap-14 py-16 sm:py-24 lg:grid-cols-[1.08fr_0.92fr] lg:items-center">
          <div className="reveal space-y-8 text-center lg:text-left">
            <Kicker>Transfert d&apos;argent rapide &amp; sécurisé</Kicker>
            <h1 className="display-title text-5xl leading-[.98] sm:text-6xl lg:text-[5rem]">
              Votre argent traverse les frontières.{" "}
              <span className="text-brand-gold">Votre confiance reste entière.</span>
            </h1>
            <div className="flex items-center justify-center gap-4 text-white/65 lg:justify-start">
              <VerticalRules className="text-brand-cyan" />
              <p className="max-w-xl text-base leading-relaxed sm:text-lg">
                Blue Sky connecte la RDC, la Zambie, la Namibie, l&apos;Afrique
                du Sud, le Zimbabwe, le Kenya, la Tanzanie et le Malawi pour
                des transferts simples, rapides et suivis.
              </p>
            </div>
            <div className="flex flex-col justify-center gap-3 sm:flex-row lg:justify-start">
              <LinkButton href="/inscription" size="lg">
                Ouvrir un compte gratuit
              </LinkButton>
              <LinkButton
                href={`https://wa.me/${SITE.whatsappNumber}`}
                target="_blank"
                variant="outline-light"
                size="lg"
              >
                Discuter sur WhatsApp
              </LinkButton>
            </div>
            <div className="flex flex-wrap justify-center gap-x-6 gap-y-3 border-t border-white/10 pt-6 text-sm text-white/65 lg:justify-start">
              <span className="flex items-center gap-2"><BadgeCheck size={17} className="text-brand-cyan" /> Transactions suivies</span>
              <span className="flex items-center gap-2"><Clock3 size={17} className="text-brand-cyan" /> Assistance réactive</span>
              <span className="flex items-center gap-2"><Globe2 size={17} className="text-brand-cyan" /> {COUNTRIES.length} pays connectés</span>
            </div>
          </div>

          <div className="reveal-delay relative mx-auto w-full max-w-lg lg:pl-10">
            <div className="absolute -left-1 top-14 z-10 rounded-2xl border border-white/15 bg-white/10 p-4 backdrop-blur-xl">
              <p className="text-3xl font-bold text-brand-gold">{COUNTRIES.length}</p>
              <p className="text-xs uppercase tracking-[.16em] text-white/60">pays desservis</p>
            </div>
            <div className="overflow-hidden rounded-[2rem] border border-white/15 bg-white/5 p-2 shadow-2xl shadow-black/30">
              <Image
                src="/images/team-photo.jpg"
                alt="L'équipe Blue Sky sur le terrain"
                width={800}
                height={900}
                className="h-[440px] w-full rounded-[1.55rem] object-cover sm:h-[540px]"
                priority
              />
            </div>
            <div className="absolute -bottom-7 right-[-.5rem] w-[82%] rounded-2xl border border-white/10 bg-surface p-5 text-text shadow-2xl">
              <p className="text-sm font-bold">Une présence humaine, sur le terrain.</p>
              <p className="mt-1 text-xs leading-relaxed text-text-muted">Des équipes locales disponibles pour vous accompagner à chaque étape.</p>
            </div>
          </div>
        </Container>
        <BlobDivider />
      </section>

      {/* Features */}
      <section className="py-24 sm:py-32">
        <Container>
          <div className="mx-auto mb-14 max-w-2xl text-center">
            <Kicker tone="blue">Pourquoi Blue Sky</Kicker>
            <h2 className="display-title mt-5 text-4xl sm:text-5xl">
              Une agence pensée pour la diaspora et les familles africaines
            </h2>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {FEATURES.map(({ icon: Icon, title, text }) => (
              <div
                key={title}
                className="premium-card group rounded-[1.5rem] p-7 transition duration-300 hover:-translate-y-1 hover:border-brand-blue/40"
              >
                <div className="mb-8 inline-flex h-12 w-12 items-center justify-center rounded-full bg-brand-blue/10 text-brand-blue transition group-hover:bg-brand-blue group-hover:text-white dark:bg-white/10 dark:text-brand-gold-light">
                  <Icon size={22} />
                </div>
                <h3 className="mb-2 text-lg font-bold">{title}</h3>
                <p className="text-sm leading-relaxed text-text-muted">{text}</p>
              </div>
            ))}
          </div>
        </Container>
      </section>

      {/* How it works */}
      <section className="border-y border-border bg-surface-muted py-24 sm:py-32">
        <Container>
          <div className="mx-auto mb-14 max-w-2xl text-center">
            <Kicker>Comment ça marche</Kicker>
            <h2 className="display-title mt-5 text-4xl sm:text-5xl">
              Trois étapes pour envoyer votre premier transfert
            </h2>
          </div>
          <div className="grid gap-8 md:grid-cols-3">
            {STEPS.map(({ icon: Icon, title, text }, i) => (
              <div key={title} className="premium-card relative rounded-[1.5rem] p-8">
                <span className="absolute -top-4 -left-2 text-6xl font-black text-brand-blue/10 dark:text-white/5">
                  0{i + 1}
                </span>
                <div className="relative mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-brand-gold text-brand-blue-deep">
                  <Icon size={22} />
                </div>
                <h3 className="relative mb-2 text-lg font-bold">{title}</h3>
                <p className="relative text-sm leading-relaxed text-text-muted">{text}</p>
              </div>
            ))}
          </div>
          <div className="mt-12 text-center">
            <LinkButton href="/inscription" size="lg">
              Commencer maintenant <ArrowRight size={18} />
            </LinkButton>
          </div>
        </Container>
      </section>

      {/* Countries */}
      <section className="py-24 sm:py-32">
        <Container>
          <div className="mx-auto mb-14 max-w-2xl text-center">
            <Kicker tone="blue">Notre couverture</Kicker>
            <h2 className="display-title mt-5 text-4xl sm:text-5xl">
              Nos agences à travers l&apos;Afrique
            </h2>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {COUNTRIES.map((country) => (
              <CountryCard key={country.code} country={country} />
            ))}
          </div>
        </Container>
      </section>

      {/* Payment partners */}
      <section className="border-y border-border bg-brand-blue-deep py-16 text-white">
        <Container>
          <p className="mb-8 text-center text-xs font-bold uppercase tracking-[.2em] text-white/50">
            Moyens de paiement &amp; partenaires mobiles
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4">
            {SITE.paymentPartners.map((partner) => (
              <span
                key={partner}
                className="rounded-full border border-white/15 bg-white/5 px-5 py-3 text-sm font-semibold text-white/80"
              >
                {partner}
              </span>
            ))}
          </div>
        </Container>
      </section>

      {/* Impact teaser */}
      <section className="py-24 sm:py-32">
        <Container className="grid items-center gap-12 lg:grid-cols-2">
          <div className="overflow-hidden rounded-[2rem] border-8 border-surface shadow-2xl">
            <Image
              src="/images/community-outreach-group.jpg"
              alt="Blue Sky aux côtés des enfants d'un orphelinat en Namibie"
              width={900}
              height={700}
              className="h-[340px] w-full object-cover sm:h-[420px]"
            />
          </div>
          <div className="space-y-5">
            <Kicker>Au-delà du transfert d&apos;argent</Kicker>
            <h2 className="display-title text-4xl sm:text-5xl">
              Nous soutenons aussi les communautés que nous servons
            </h2>
            <p className="leading-relaxed text-text-muted">
              L&apos;équipe Blue Sky se rend régulièrement auprès d&apos;enfants
              d&apos;un orphelinat en Namibie pour offrir du temps, des
              ressources et du soutien — parce que connecter les familles va
              au-delà des transactions.
            </p>
            <LinkButton href="/impact" variant="ghost">
              Découvrir notre impact <ArrowRight size={16} />
            </LinkButton>
          </div>
        </Container>
      </section>

      {/* Final CTA */}
      <section className="subtle-grid bg-brand-blue-deep py-20 text-white sm:py-24">
        <Container className="text-center">
          <Kicker>Commencez aujourd&apos;hui</Kicker>
          <h2 className="display-title mx-auto mt-5 max-w-3xl text-4xl sm:text-5xl">
            Prêt à envoyer votre argent en toute confiance ?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-white/70">
            Ouvrez votre compte Blue Sky gratuitement et suivez chacun de vos
            transferts depuis votre tableau de bord.
          </p>
          <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
            <LinkButton href="/inscription" size="lg">
              Ouvrir un compte gratuit
            </LinkButton>
            <LinkButton href="/contact" variant="outline-light" size="lg">
              Nous contacter
            </LinkButton>
          </div>
        </Container>
      </section>
    </>
  );
}
