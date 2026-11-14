SITE = {
    "name": "Blue Sky",
    "tagline": "Transférez votre argent en toute confiance et sécurité",
    "primary_email": "bluesky@gmail.com",
    "secondary_email": "blueskyafrica01@gmail.com",
    "primary_phone": "+243 972 113 974",
    "whatsapp_number": "243972113974",
    "whatsapp_display": "+243 972 113 974",
    "head_office_address": (
        "Avenue Kapenda & Mobutu, Quartier Makutano, Commune de Lubumbashi, "
        "Haut-Katanga (RDC), en face de l'Hôtel Hypnose"
    ),
    "social": {
        "tiktok": "https://www.tiktok.com/@africa_bluesky",
        "facebook": "https://www.facebook.com/profile.php?id=61588726012210",
        "instagram": "https://www.instagram.com/reel/Dam1JrQKAHQ/?igsh=MTRiZzZqOXV2NWd4Nw==",
    },
    "mission": (
        "Connecter les pays, les continents et les monnaies à une seule table qui est "
        "Blue Sky, et rendre les services de transfert accessibles à toutes les "
        "catégories confondues."
    ),
    "purpose": (
        "Faciliter l'envoi et la réception d'argent à l'international en garantissant "
        "la rapidité et l'efficacité."
    ),
    "definition": (
        "Blue Sky est une agence de transfert d'argent spécialisée dans les "
        "transactions internationales entre la République Démocratique du Congo, la "
        "Namibie, la Zambie, l'Afrique du Sud, le Zimbabwe, le Kenya, l'Ouganda, la "
        "Tanzanie et le Malawi. Nous offrons des solutions rapides, fiables et "
        "sécurisées pour envoyer et recevoir de l'argent à travers ces pays."
    ),
    "payment_partners": [
        "M-Pesa",
        "Orange Money",
        "Airtel Money",
        "MTN Money",
        "Equity BCDC",
        "Illicocash",
        "PMobile",
        "Pays2Cell",
        "eWallet",
    ],
    "savings_tagline": "Épargnez sereinement, à votre rythme",
    "savings_description": (
        "En plus du transfert d'argent, Blue Sky propose une branche Épargne : "
        "un moyen simple et sécurisé de mettre de l'argent de côté pour vos études, "
        "votre famille ou votre activité. Vous êtes enregistré dans notre programme "
        "d'épargne et vous pouvez suivre votre compte à tout moment, avec le même "
        "accompagnement humain qu'en agence."
    ),
}

COUNTRIES = [
    {
        "code": "CD",
        "name": "Congo (RDC)",
        "flag": "🇨🇩",
        "address": (
            "Avenue Kapenda, Coins Mobutu, en face de l'Hôtel Hypnose, Quartier "
            "Makutano, Commune de Lubumbashi, Haut-Katanga"
        ),
        "phones": ["+243 972 113 974", "+243 989 555 229"],
        "note": "",
    },
    {
        "code": "ZM",
        "name": "Zambie",
        "flag": "🇿🇲",
        "address": "Inter City Bus Station",
        "phones": ["+260 771 306 147", "+260 974 909 125", "+260 773 144 727"],
        "note": "Airtel Money & MTN Money disponibles sur place",
    },
    {
        "code": "NA",
        "name": "Namibie",
        "flag": "🇳🇦",
        "address": "3 Weber Street, Windhoek, près de l'entrée principale de NUST",
        "phones": ["+264 857 681 484"],
        "note": "",
    },
    {
        "code": "ZA",
        "name": "Afrique du Sud",
        "flag": "🇿🇦",
        "address": "",
        "phones": ["+243 972 113 974"],
        "note": "",
    },
    {
        "code": "TZ",
        "name": "Tanzanie",
        "flag": "🇹🇿",
        "address": "Marché Kariakoo",
        "phones": ["+255 745 157 262"],
        "note": "",
    },
    {
        "code": "KE",
        "name": "Kenya",
        "flag": "🇰🇪",
        "address": "",
        "phones": ["+254 117 194 191"],
        "note": "Envoyez de l'argent au Kenya facilement, rapidement et en toute sécurité.",
    },
    {
        "code": "UG",
        "name": "Ouganda",
        "flag": "🇺🇬",
        "address": "Kampala",
        "phones": ["+243 972 113 974"],
        "note": "Nouvelle agence",
    },
    {
        "code": "ZW",
        "name": "Zimbabwe",
        "flag": "🇿🇼",
        "address": "Africa University, Mutare",
        "phones": ["+243 974 344 310"],
        "note": "",
    },
    {
        "code": "MW",
        "name": "Malawi",
        "flag": "🇲🇼",
        "address": "Lilongwe, Area 47 / Secteur 3 No. 15",
        "phones": ["+265 992 040 049"],
        "note": "",
    },
]

CURRENCIES = ["USD", "CDF", "ZMW", "NAD", "ZAR", "KES", "UGX", "TZS", "MWK"]


# Capital-city photography for the country cards (static/img/capitals/<code>.jpg).
# Keyed by ISO code so it works for both the Agency model and the static
# COUNTRIES fallback. Photos come from Wikimedia Commons under free licences;
# the credit fields are rendered on the countries page as attribution.
CAPITALS = {
    "CD": {
        "city": "Kinshasa",
        "image": "img/capitals/cd.jpg",
        "position": "center 60%",
        "credit": "Francis Shok Mweze",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:La_Gombe,_Kinshasa,_RDC_(cropped).jpg",
    },
    "ZM": {
        "city": "Lusaka",
        "image": "img/capitals/zm.jpg",
        "position": "center 40%",
        "credit": "Matthew Grollnek",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Downtown_Lusaka.JPG",
    },
    "NA": {
        "city": "Windhoek",
        "image": "img/capitals/na.jpg",
        "position": "center 55%",
        "credit": "Christoph Strässler",
        "license": "CC BY-SA 2.0",
        "source": "https://commons.wikimedia.org/wiki/File:Christ_Church_in_Windhoek,_Namibia.jpg",
    },
    "ZA": {
        "city": "Pretoria",
        "image": "img/capitals/za.jpg",
        "position": "center 45%",
        "credit": "Davinci77",
        "license": "CC BY-SA 3.0",
        "source": "https://commons.wikimedia.org/wiki/File:Uniegebou.jpg",
    },
    "TZ": {
        "city": "Dodoma",
        "image": "img/capitals/tz.jpg",
        "position": "center 40%",
        "credit": "Mangapwani",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Street_in_Viwandani_ward,_Dodoma_City.jpg",
    },
    "KE": {
        "city": "Nairobi",
        "image": "img/capitals/ke.jpg",
        "position": "center 55%",
        "credit": "Daniel Case",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Nairobi_skyline_from_Gem_Hotel.jpg",
    },
    "UG": {
        "city": "Kampala",
        "image": "img/capitals/ug.jpg",
        "position": "center 70%",
        "credit": "Chapelle musa",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Urban_Rising,_KAMPALA,_Uganda.jpg",
    },
    "ZW": {
        "city": "Harare",
        "image": "img/capitals/zw.jpg",
        "position": "center 35%",
        "credit": "Baynham Goredema",
        "license": "CC BY 2.0",
        "source": "https://commons.wikimedia.org/wiki/File:Crowne_Plaza,_Harare.png",
    },
    "MW": {
        "city": "Lilongwe",
        "image": "img/capitals/mw.jpg",
        "position": "center 40%",
        "credit": "Felixfeld",
        "license": "CC BY-SA 3.0",
        "source": "https://commons.wikimedia.org/wiki/File:K.a.r-.clocktower-in-lilongwe.jpg",
    },
}
