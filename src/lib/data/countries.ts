export type CountryOffice = {
  code: string;
  name: string;
  flag: string;
  address: string;
  phones: string[];
  note?: string;
};

export const COUNTRIES: CountryOffice[] = [
  {
    code: "CD",
    name: "Congo (RDC)",
    flag: "🇨🇩",
    address:
      "Avenue Kapenda, Coins Mobutu — en face de l'Hôtel Hypnose, Quartier Makutano, Commune de Lubumbashi, Haut-Katanga",
    phones: ["+243 972 113 974", "+243 989 555 229"],
  },
  {
    code: "ZM",
    name: "Zambie",
    flag: "🇿🇲",
    address: "Inter City Bus Station",
    phones: ["+260 771 306 147", "+260 974 909 125", "+260 773 144 727"],
    note: "Airtel Money & MTN Money disponibles sur place",
  },
  {
    code: "NA",
    name: "Namibie",
    flag: "🇳🇦",
    address: "Windhoek",
    phones: ["+264 857 681 484"],
  },
  {
    code: "ZA",
    name: "Afrique du Sud",
    flag: "🇿🇦",
    address: "Transaction électronique",
    phones: ["+243 972 113 974"],
  },
  {
    code: "TZ",
    name: "Tanzanie",
    flag: "🇹🇿",
    address: "Marché Kariakoo",
    phones: ["+255 745 157 262"],
  },
  {
    code: "KE",
    name: "Kenya",
    flag: "🇰🇪",
    address: "Transaction électronique",
    phones: ["+254 117 194 191"],
  },
  {
    code: "ZW",
    name: "Zimbabwe",
    flag: "🇿🇼",
    address: "Africa University, Mutare",
    phones: ["+243 974 344 310"],
  },
  {
    code: "MW",
    name: "Malawi",
    flag: "🇲🇼",
    address: "Lilongwe, Area 47 / Secteur 3 No. 15",
    phones: ["+265 992 040 049"],
  },
];
