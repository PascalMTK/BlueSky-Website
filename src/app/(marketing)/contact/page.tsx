import type { Metadata } from "next";
import { Mail, Phone, MapPin, MessageCircle } from "lucide-react";
import { Container } from "@/components/ui/container";
import { Kicker } from "@/components/ui/kicker";
import { ContactForm } from "@/components/forms/contact-form";
import { SITE } from "@/lib/data/site";

export const metadata: Metadata = {
  title: "Contact",
  description:
    "Contactez l'équipe Blue Sky par téléphone, WhatsApp, e-mail ou via notre formulaire en ligne.",
};

export default function ContactPage() {
  return (
    <>
      <section className="bg-brand-blue py-16 text-white sm:py-20">
        <Container className="text-center">
          <Kicker>Parlons-en</Kicker>
          <h1 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold sm:text-5xl">
            Une question ? Notre équipe vous répond
          </h1>
        </Container>
      </section>

      <section className="py-20 sm:py-28">
        <Container className="grid gap-14 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="space-y-6">
            <div className="flex items-start gap-4 rounded-2xl border border-border bg-surface p-6">
              <MapPin className="mt-0.5 shrink-0 text-brand-blue dark:text-brand-gold-light" size={22} />
              <div>
                <p className="font-bold">Siège social</p>
                <p className="text-sm text-text-muted">{SITE.headOfficeAddress}</p>
              </div>
            </div>
            <div className="flex items-start gap-4 rounded-2xl border border-border bg-surface p-6">
              <Phone className="mt-0.5 shrink-0 text-brand-blue dark:text-brand-gold-light" size={22} />
              <div>
                <p className="font-bold">Téléphone</p>
                <p className="text-sm text-text-muted">{SITE.primaryPhone}</p>
              </div>
            </div>
            <div className="flex items-start gap-4 rounded-2xl border border-border bg-surface p-6">
              <Mail className="mt-0.5 shrink-0 text-brand-blue dark:text-brand-gold-light" size={22} />
              <div>
                <p className="font-bold">E-mail</p>
                <p className="text-sm text-text-muted">{SITE.primaryEmail}</p>
              </div>
            </div>
            <a
              href={`https://wa.me/${SITE.whatsappNumber}`}
              target="_blank"
              rel="noreferrer noopener"
              className="flex items-center gap-4 rounded-2xl bg-[#25D366] p-6 text-white transition hover:-translate-y-0.5"
            >
              <MessageCircle size={22} />
              <div>
                <p className="font-bold">WhatsApp</p>
                <p className="text-sm text-white/80">{SITE.whatsappDisplay}</p>
              </div>
            </a>
          </div>

          <ContactForm />
        </Container>
      </section>
    </>
  );
}
