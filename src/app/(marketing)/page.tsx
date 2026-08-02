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
  ArrowDown,
  LockKeyhole,
  CircleDollarSign,
} from "lucide-react";
import { Container } from "@/components/ui/container";
import { Kicker } from "@/components/ui/kicker";
import { LinkButton } from "@/components/ui/button";
import { CountryCard } from "@/components/country-card";
import { TiltCard } from "@/components/ui/tilt-card";
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
      <section className="hero-mesh relative overflow-hidden text-white">
        <div aria-hidden className="hero-photo-merge">
          <Image
            src="/images/team-photo.jpg"
            alt=""
            fill
            priority
            sizes="100vw"
          />
        </div>
        <div aria-hidden className="subtle-grid absolute inset-0 opacity-60" />
        <div aria-hidden className="orb orb-slow bg-brand-gold/25 h-72 w-72 -top-10 right-[8%]" />
        <div aria-hidden className="orb orb-delay bg-brand-cyan/20 h-64 w-64 bottom-[6%] left-[4%]" />
        <Container className="relative grid min-h-[700px] gap-16 py-16 sm:py-20 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:py-24">
          <div className="reveal text-center lg:text-left">
            <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/[.07] px-4 py-2 text-xs font-semibold text-white/80 backdrop-blur">
              <span className="h-2 w-2 rounded-full bg-brand-cyan shadow-[0_0_0_5px_rgba(85,216,255,.12)]" />
              Transferts internationaux, simplement
            </div>
            <h1 className="display-title max-w-3xl text-5xl leading-[.98] sm:text-6xl lg:text-[4.75rem]">
              L&apos;argent arrive. <span className="text-brand-gold">La confiance aussi.</span>
            </h1>
            <p className="mx-auto mt-7 max-w-xl text-base leading-relaxed text-white/68 sm:text-lg lg:mx-0">
              Envoyez de l&apos;argent à vos proches dans {COUNTRIES.length} pays africains avec un suivi clair et une équipe disponible à chaque étape.
            </p>
            <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row lg:justify-start">
              <LinkButton href="/inscription" size="lg">
                Commencer un transfert <ArrowRight size={18} />
              </LinkButton>
              <LinkButton
                href={`https://wa.me/${SITE.whatsappNumber}`}
                target="_blank"
                variant="outline-light"
                size="lg"
              >
                Parler à un conseiller
              </LinkButton>
            </div>
            <div className="mt-9 flex flex-wrap justify-center gap-x-7 gap-y-3 border-t border-white/10 pt-6 text-xs font-semibold text-white/60 lg:justify-start">
              <span className="flex items-center gap-2"><LockKeyhole size={15} className="text-brand-cyan" /> Données protégées</span>
              <span className="flex items-center gap-2"><BadgeCheck size={15} className="text-brand-cyan" /> Transfert suivi</span>
              <span className="flex items-center gap-2"><Headset size={15} className="text-brand-cyan" /> Support humain</span>
            </div>
          </div>

          <div className="reveal-delay mx-auto w-full max-w-[490px]">
            <TiltCard intensity={6} className="rounded-[1.75rem]">
              <div className="glass-panel rounded-[1.75rem] p-4 shadow-[0_40px_90px_-30px_rgba(0,0,0,.75)] sm:p-6">
                <div className="mb-6 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[.16em] text-white/45">Simulation instantanée</p>
                    <h2 className="mt-1 font-sans text-xl font-bold tracking-tight">Envoyer de l&apos;argent</h2>
                  </div>
                  <span className="coin-3d flex h-11 w-11 items-center justify-center rounded-xl bg-brand-gold text-brand-blue-deep">
                    <span className="coin-3d-spin flex"><CircleDollarSign size={22} /></span>
                  </span>
                </div>
                <div className="route-line">
                  <div className="rounded-2xl border border-white/10 bg-white/[.08] p-4">
                    <p className="text-xs text-white/50">Vous envoyez</p>
                    <div className="mt-2 flex items-end justify-between gap-4">
                      <span className="text-3xl font-bold tracking-tight">500.00</span>
                      <span className="rounded-lg bg-white/10 px-3 py-2 text-sm font-bold">USD</span>
                    </div>
                  </div>
                  <span className="absolute left-1 top-[75px] z-10 flex h-8 w-8 items-center justify-center rounded-full border-4 border-[#163765] bg-brand-gold text-brand-blue-deep"><ArrowDown size={14} strokeWidth={3} /></span>
                </div>
                <div className="mt-4 rounded-2xl border border-white/10 bg-white/[.08] p-4">
                  <p className="text-xs text-white/50">Votre proche reçoit</p>
                  <div className="mt-2 flex items-end justify-between gap-4">
                    <span className="text-3xl font-bold tracking-tight">—</span>
                    <span className="rounded-lg bg-white/10 px-3 py-2 text-sm font-bold">CDF</span>
                  </div>
                </div>
                <div className="my-5 grid grid-cols-2 gap-3 text-xs">
                  <div className="rounded-xl bg-black/10 p-3"><p className="text-white/45">Destination</p><p className="mt-1 font-semibold">R.D. Congo</p></div>
                  <div className="rounded-xl bg-black/10 p-3"><p className="text-white/45">Délai estimé</p><p className="mt-1 font-semibold">Quelques minutes</p></div>
                </div>
                <LinkButton href="/inscription" size="lg" className="w-full">Voir mon estimation <ArrowRight size={17} /></LinkButton>
                <p className="mt-4 flex items-center justify-center gap-2 text-[11px] text-white/45"><LockKeyhole size={12} /> Aucun engagement · estimation gratuite</p>
              </div>
            </TiltCard>
          </div>
        </Container>
        <div className="relative border-t border-white/10 bg-black/10">
          <Container className="grid grid-cols-2 divide-x divide-white/10 py-5 sm:grid-cols-4">
            {[['8', 'pays connectés'], ['7', 'moyens de paiement'], ['100%', 'suivi personnalisé'], ['1', 'équipe à votre écoute']].map(([value, label]) => (
              <div key={label} className="px-3 py-3 text-center"><p className="text-xl font-bold text-white">{value}</p><p className="mt-1 text-[10px] uppercase tracking-[.12em] text-white/45">{label}</p></div>
            ))}
          </Container>
        </div>
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
              <TiltCard key={title} intensity={8} className="rounded-[1.5rem]">
                <div className="premium-card group rounded-[1.5rem] p-7 transition-colors duration-300 hover:border-brand-blue/40">
                  <div className="mb-8 inline-flex h-12 w-12 items-center justify-center rounded-full bg-brand-blue/10 text-brand-blue transition group-hover:bg-brand-blue group-hover:text-white dark:bg-white/10 dark:text-brand-gold-light">
                    <Icon size={22} />
                  </div>
                  <h3 className="mb-2 text-lg font-bold">{title}</h3>
                  <p className="text-sm leading-relaxed text-text-muted">{text}</p>
                </div>
              </TiltCard>
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
              <TiltCard key={title} intensity={7} className="rounded-[1.5rem]">
                <div className="premium-card relative rounded-[1.5rem] p-8">
                  <span className="absolute -top-4 -left-2 text-6xl font-black text-brand-blue/10 dark:text-white/5">
                    0{i + 1}
                  </span>
                  <div className="relative mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-brand-gold text-brand-blue-deep">
                    <Icon size={22} />
                  </div>
                  <h3 className="relative mb-2 text-lg font-bold">{title}</h3>
                  <p className="relative text-sm leading-relaxed text-text-muted">{text}</p>
                </div>
              </TiltCard>
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
              <TiltCard key={country.code} intensity={7} className="rounded-[1.5rem]">
                <CountryCard country={country} />
              </TiltCard>
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
          <TiltCard intensity={5} glare={false} className="image-merge-wrap">
            <Image
              src="/images/community-outreach-group.jpg"
              alt="Blue Sky aux côtés des enfants d'un orphelinat en Namibie"
              width={900}
              height={700}
              className="image-merge h-[340px] w-full object-cover sm:h-[420px]"
            />
          </TiltCard>
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
