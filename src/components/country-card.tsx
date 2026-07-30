import { Phone, MapPin } from "lucide-react";
import type { CountryOffice } from "@/lib/data/countries";

export function CountryCard({ country }: { country: CountryOffice }) {
  return (
    <div className="premium-card group rounded-[1.5rem] p-6 transition duration-300 hover:-translate-y-1 hover:border-brand-blue/40">
      <div className="mb-4 flex items-center gap-3">
        <span className="text-3xl">{country.flag}</span>
        <h3 className="text-lg font-bold">{country.name}</h3>
      </div>
      <p className="mb-3 flex items-start gap-2 text-sm text-text-muted">
        <MapPin size={16} className="mt-0.5 shrink-0 text-brand-blue dark:text-brand-gold-light" />
        {country.address}
      </p>
      <ul className="space-y-1.5">
        {country.phones.map((phone) => (
          <li key={phone} className="flex items-center gap-2 text-sm font-semibold">
            <Phone size={14} className="shrink-0 text-brand-blue dark:text-brand-gold-light" />
            {phone}
          </li>
        ))}
      </ul>
      {country.note && (
        <p className="mt-3 text-xs text-text-muted">{country.note}</p>
      )}
    </div>
  );
}
