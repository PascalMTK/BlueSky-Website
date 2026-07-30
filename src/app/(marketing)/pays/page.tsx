import type { Metadata } from "next";
import { Container } from "@/components/ui/container";
import { Kicker } from "@/components/ui/kicker";
import { CountryCard } from "@/components/country-card";
import { COUNTRIES } from "@/lib/data/countries";

export const metadata: Metadata = {
  title: "Nos agences",
  description:
    "Retrouvez les coordonnées de toutes les agences Blue Sky en RDC, Zambie, Namibie, Afrique du Sud, Zimbabwe, Kenya, Tanzanie et Malawi.",
};

export default function CountriesPage() {
  return (
    <>
      <section className="bg-brand-blue py-16 text-white sm:py-20">
        <Container className="text-center">
          <Kicker>Nos agences</Kicker>
          <h1 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold sm:text-5xl">
            Blue Sky, présent dans {COUNTRIES.length} pays d&apos;Afrique
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-white/70">
            Contactez directement l&apos;agence la plus proche de vous, ou
            démarrez votre transfert en ligne depuis votre compte Blue Sky.
          </p>
        </Container>
      </section>

      <section className="py-20 sm:py-28">
        <Container>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {COUNTRIES.map((country) => (
              <CountryCard key={country.code} country={country} />
            ))}
          </div>
        </Container>
      </section>
    </>
  );
}
