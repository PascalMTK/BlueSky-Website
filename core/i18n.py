"""
Lightweight, dependency-free translation system.

Why not Django's built-in gettext i18n? It needs the GNU gettext binaries
(xgettext to extract strings, msgfmt to compile .po -> .mo) which aren't
available in this project's environment, and pulling in a paid third-party
translation API was explicitly ruled out. So page copy is translated
through a plain Python dictionary per language below, looked up by the
`{% t %}` / `{% blockt %}` template tags (see
core/templatetags/i18n_extra.py) and served via LanguageMiddleware
(core/middleware.py).

French is the language the site is actually written in, so it needs no
dictionary — it's also the fallback for any string that has no translation
yet in another language, so a missing entry never renders blank or breaks
the page; it just quietly shows French until someone fills it in.

To add a language: add a row to AVAILABLE_LANGUAGES and give it a dict in
TRANSLATIONS. To translate a new string: wrap it in `{% t "..." %}` (plain
text) or `{% blockt %}...{% endblockt %}` (text that contains inline HTML,
e.g. a <span> highlight) in the template, then add the exact French text as
the dict key and the translation as the value, for each language.
"""

AVAILABLE_LANGUAGES = [
    {"code": "fr", "label": "Français", "flag": "🇫🇷"},
    {"code": "en", "label": "English", "flag": "🇬🇧"},
    {"code": "sw", "label": "Kiswahili", "flag": "🇹🇿"},
]
SOURCE_LANGUAGE = "fr"

TRANSLATIONS = {
    "en": {
        # --- header / nav ---
        "Accueil": "Home",
        "À propos": "About",
        "Équipe": "Team",
        "Actualités": "News",
        "Nos pays": "Our countries",
        "Épargne": "Savings",
        "Lun–Sam : 08h00–18h00": "Mon–Sat: 08:00–18:00",
        "Basculer le mode sombre": "Toggle dark mode",
        "Nous contacter": "Contact us",

        # --- footer ---
        "Blue Sky / Afrique australe": "Blue Sky / Southern Africa",
        "L'argent voyage.": "Money travels.",
        "La confiance reste.": "Trust stays.",
        "Notre équipe": "Our team",
        "Notre impact": "Our impact",
        "Nos agences": "Our branches",
        "Contact direct": "Direct contact",
        "Tous droits réservés.": "All rights reserved.",
        "Présent dans": "Present in",
        "pays": "countries",

        # --- country names (shared across footer, cards, forms) ---
        "Congo (RDC)": "DR Congo",
        "Zambie": "Zambia",
        "Namibie": "Namibia",
        "Afrique du Sud": "South Africa",
        "Tanzanie": "Tanzania",
        "Ouganda": "Uganda",

        # --- country cards (core/templates/core/partials/country_card.html) ---
        "Drapeau de": "Flag of",
        "Agence": "Branch",
        "Transfert digital": "Digital transfer",
        "Adresse & contacts": "Address & contacts",
        "Adresse de l'agence": "Branch address",
        "Service de transfert électronique": "Electronic transfer service",
        "Effectuez vos opérations à distance avec l'accompagnement direct de notre équipe. Un point d'accueil physique sera annoncé prochainement.":
            "Carry out your transactions remotely with direct support from our team. A physical location will be announced soon.",
        "Téléphone & WhatsApp": "Phone & WhatsApp",
        "Airtel Money & MTN Money disponibles sur place": "Airtel Money & MTN Money available on site",
        "Envoyez de l'argent au Kenya facilement, rapidement et en toute sécurité.":
            "Send money to Kenya easily, quickly, and securely.",
        "Nouvelle agence": "New branch",

        # --- homepage: hero ---
        "Le transfert qui nous rapproche": "The transfer that brings us closer",
        'Envoyez plus loin.<br><span class="text-brand-blue">Restez plus proche.</span>':
            'Send further.<br><span class="text-brand-blue">Stay closer.</span>',
        "Envoyez de l'argent dans": "Send money to",
        "pays africains avec un suivi transparent, un accompagnement humain et la sérénité à chaque étape.":
            "African countries with transparent tracking, human support, and peace of mind at every step.",
        "Parler à un conseiller": "Talk to an advisor",
        "Un accompagnement humain": "Human support",
        "avant, pendant et après chaque transfert": "before, during, and after every transfer",
        "Données protégées": "Protected data",
        "Transfert suivi": "Tracked transfer",
        "Support humain": "Human support",
        "Envoyer de l'argent": "Send money",
        "Vous envoyez": "You send",
        "Demander un devis": "Request a quote",

        # --- homepage: construction CTA ---
        'Construisez votre avenir en toute <span class="text-brand-gold">sécurité</span> et en toute <span class="text-brand-gold">confiance</span> avec Blue Sky':
            'Build your future in complete <span class="text-brand-gold">safety</span> and <span class="text-brand-gold">confidence</span> with Blue Sky',
        "Qu'il s'agisse de financer un projet de construction, de soutenir votre famille ou de faire grandir votre activité, Blue Sky vous accompagne dans":
            "Whether you're financing a construction project, supporting your family, or growing your business, Blue Sky supports you across",
        "pays d'Afrique avec la même rigueur à chaque transfert.": "African countries with the same rigor on every transfer.",
        "Nous contacter pour ce service": "Contact us about this service",

        # --- homepage: services ---
        "Bâtissons ensemble": "Let's build together",
        "Pourquoi Blue Sky": "Why Blue Sky",
        "Des services construits autour de la confiance": "Services built around trust",
        "Une présence locale, un suivi transparent et une équipe disponible pour que chaque transfert reste simple du départ à l'arrivée.":
            "A local presence, transparent tracking, and a team on hand so every transfer stays simple from start to finish.",
        "Découvrir": "Discover",
        "100% sécurisé": "100% secure",
        "Chaque transaction est protégée et suivie de bout en bout, sans mauvaise surprise.":
            "Every transaction is protected and tracked end to end, with no surprises.",
        "Ultra rapide": "Ultra fast",
        "Vos bénéficiaires reçoivent leurs fonds en quelques minutes, pas en quelques jours.":
            "Your recipients get their funds in minutes, not days.",
        "Réseau régional": "Regional network",
        "9 pays d'Afrique australe et de l'Est connectés à une seule plateforme.":
            "9 African countries across Southern and East Africa connected on one platform.",
        "Assistance humaine": "Human assistance",
        "Une équipe joignable sur WhatsApp et par téléphone, dans chaque pays où nous opérons.":
            "A team reachable on WhatsApp and by phone, in every country where we operate.",

        # --- homepage: steps ---
        "Comment ça marche": "How it works",
        "Trois étapes pour envoyer votre premier transfert": "Three steps to send your first transfer",
        "Étape": "Step",
        "Créez votre compte": "Create your account",
        "Inscription en quelques minutes pour accéder à votre tableau de bord Blue Sky.":
            "Sign up in minutes to access your Blue Sky dashboard.",
        "Ajoutez un bénéficiaire": "Add a recipient",
        "Enregistrez les informations de la personne qui recevra les fonds.":
            "Save the details of the person who will receive the funds.",
        "Envoyez en toute confiance": "Send with confidence",
        "Choisissez le montant et le moyen de paiement, nous nous occupons du reste.":
            "Choose the amount and payment method, we handle the rest.",

        # --- homepage: countries + partners ---
        "Notre couverture": "Our coverage",
        "Nos agences à travers l'Afrique": "Our branches across Africa",
        "Moyens de paiement &amp; partenaires mobiles": "Payment methods &amp; mobile partners",

        # --- homepage: savings ---
        "Épargner un peu, chaque mois": "Save a little, every month",
        "Notre branche Épargne": "Our Savings branch",
        "Épargnez sereinement, à votre rythme": "Save with peace of mind, at your own pace",
        (
            "En plus du transfert d'argent, Blue Sky propose une branche Épargne : "
            "un moyen simple et sécurisé de mettre de l'argent de côté pour vos études, "
            "votre famille ou votre activité. Vous êtes enregistré dans notre programme "
            "d'épargne et vous pouvez suivre votre compte à tout moment, avec le même "
            "accompagnement humain qu'en agence."
        ): (
            "In addition to money transfer, Blue Sky offers a Savings service: a simple, "
            "secure way to set money aside for your studies, your family, or your business. "
            "You're registered in our savings program and can track your account at any "
            "time, with the same human support you'd get in branch."
        ),
        "Étudiants": "Students",
        "Mettez de côté pour vos frais académiques et vos projets d'avenir, à votre rythme.":
            "Set money aside for your school fees and future plans, at your own pace.",
        "Familles": "Families",
        "Construisez un fonds commun pour les imprévus, les études des enfants ou un projet familial.":
            "Build a shared fund for emergencies, your children's education, or a family project.",
        "Entreprises": "Businesses",
        "Épargnez pour votre fonds de roulement ou vos investissements, avec un suivi dédié.":
            "Save for your working capital or investments, with dedicated tracking.",
        "S'enrôler au service épargne": "Sign up for Savings",
        "Ou écrivez-nous directement sur": "Or write to us directly on",

        # --- homepage: hero stats ---
        "pays connectés": "countries connected",
        "moyens de paiement": "payment methods",
        "suivi personnalisé": "personalized tracking",
        "équipe à votre écoute": "team ready to help",

        # --- homepage: community / impact ---
        "pays reliés par une même équipe": "countries connected by one team",
        "Au-delà du transfert d'argent": "Beyond money transfer",
        "Une expertise locale, portée par des relations humaines": "Local expertise, powered by human relationships",
        (
            "L'équipe Blue Sky se rend régulièrement auprès d'enfants d'un orphelinat en "
            "Namibie pour offrir du temps, des ressources et du soutien — parce que "
            "connecter les familles va au-delà des transactions."
        ): (
            "The Blue Sky team regularly visits children at an orphanage in Namibia to "
            "offer time, resources, and support — because connecting families goes beyond "
            "transactions."
        ),
        "Présence locale": "Local presence",
        "Des équipes sur le terrain, pas seulement en ligne.": "Teams on the ground, not just online.",
        "Impact direct": "Direct impact",
        "Du temps et des ressources pour les communautés locales.": "Time and resources for local communities.",
        "Engagement communautaire": "Community engagement",
        "Découvrir notre impact": "Discover our impact",

        # --- homepage: final CTA ---
        "Commencez aujourd'hui": "Get started today",
        "Prêt à envoyer votre argent en toute confiance ?": "Ready to send your money with confidence?",
        "Contactez l'équipe Blue Sky ou rendez-vous dans l'agence la plus proche pour démarrer votre transfert.":
            "Contact the Blue Sky team or visit the nearest branch to start your transfer.",
        "Appelez-nous": "Call us",
        "Nous écrire": "Write to us",
        "Trouver une agence": "Find a branch",

        # --- shared form fields/errors (core/_field.html, core/_form_errors.html) ---
        "Nom complet": "Full name",
        "Entrez votre nom complet": "Enter your full name",
        "Adresse e-mail": "Email address",
        "Adresse e-mail invalide": "Invalid email address",
        "Téléphone": "Phone",
        "Numéro de téléphone invalide": "Invalid phone number",
        "Pays": "Country",
        "Sélectionnez votre pays": "Select your country",
        "Mot de passe": "Password",
        "Le mot de passe doit contenir au moins 8 caractères": "Password must be at least 8 characters",
        "Un compte existe déjà avec cette adresse e-mail.": "An account already exists with this email address.",
        "Adresse e-mail déjà utilisée": "Email address already in use",
        "Adresse e-mail ou mot de passe invalide.": "Invalid email address or password.",
        "Merci de corriger les champs indiqués.": "Please correct the fields indicated.",
        "Sujet de votre demande": "Subject of your request",
        "Votre message": "Your message",
        "Votre message est un peu court": "Your message is a bit short",

        # --- auth: base_auth / login / signup ---
        "Un réseau. Huit pays.": "One network. Eight countries.",
        'L\'argent arrive.<br>La confiance aussi.': 'Money arrives.<br>So does trust.',
        "Connexion": "Log in",
        "Accédez à votre tableau de bord Blue Sky.": "Access your Blue Sky dashboard.",
        "Se connecter": "Log in",
        "Pas encore de compte ?": "Don't have an account yet?",
        "Ouvrir un compte": "Open an account",
        "Quelques minutes suffisent": "It only takes a few minutes",
        'Notez vos infos.<br>On s\'occupe du reste.': 'Jot down your details.<br>We take it from there.',
        "Créez votre compte Blue Sky en quelques minutes.": "Create your Blue Sky account in minutes.",
        "Créer mon compte": "Create my account",
        "Déjà un compte ?": "Already have an account?",

        # --- about ---
        "Une agence bâtie pour rapprocher les familles africaines": "An agency built to bring African families closer",
        "Notre but": "Our purpose",
        "Notre mission": "Our mission",
        "L'équipe de direction, Blue Sky": "The leadership team, Blue Sky",
        "Cette vision guide chacune de nos décisions : ouvrir de nouvelles agences là où les familles en ont besoin, simplifier chaque étape du transfert, et rester joignables humainement, pas seulement via une application.":
            "This vision guides every one of our decisions: opening new branches where families need them, simplifying every step of a transfer, and staying reachable by real people, not just an app.",
        "&laquo; Nous voulons qu'aucune distance, aucune frontière n'empêche une famille de prendre soin des siens. Blue Sky existe pour que chaque franc, chaque kwacha, chaque rand envoyé arrive à destination avec la même confiance qu'une remise en main propre. &raquo;":
            "&laquo; We want no distance, no border, to stop a family from taking care of its own. Blue Sky exists so that every franc, every kwacha, every rand sent arrives with the same trust as if it were handed over in person. &raquo;",
        (
            "Blue Sky est une agence de transfert d'argent spécialisée dans les "
            "transactions internationales entre la République Démocratique du Congo, la "
            "Namibie, la Zambie, l'Afrique du Sud, le Zimbabwe, le Kenya, l'Ouganda, la "
            "Tanzanie et le Malawi. Nous offrons des solutions rapides, fiables et "
            "sécurisées pour envoyer et recevoir de l'argent à travers ces pays."
        ): (
            "Blue Sky is a money transfer agency specializing in international "
            "transactions between the Democratic Republic of Congo, Namibia, Zambia, "
            "South Africa, Zimbabwe, Kenya, Uganda, Tanzania, and Malawi. We offer fast, "
            "reliable, and secure solutions for sending and receiving money across these "
            "countries."
        ),
        (
            "Faciliter l'envoi et la réception d'argent à l'international en garantissant "
            "la rapidité et l'efficacité."
        ): (
            "Making international money transfers easier by guaranteeing speed and "
            "efficiency."
        ),

        # --- team ---
        "Des visages humains derrière vos transferts": "Real people behind every transfer",
        "Derrière chaque transfert Blue Sky, une équipe ancrée en Afrique australe veille chaque jour à ce que votre argent arrive vite et en toute sécurité.":
            "Behind every Blue Sky transfer, a team rooted in Southern Africa makes sure your money arrives fast and safely, every day.",
        "Proximité & Terrain": "Close to you, on the ground",
        "Une présence locale forte dans chaque agence.": "A strong local presence in every branch.",
        "Notre équipe combine des profils opérationnels, un service client réactif et des agents locaux répartis dans nos":
            "Our team combines operations staff, responsive customer service, and local agents spread across our",
        "de couverture — de Lubumbashi à Windhoek, en passant par Lusaka et Lilongwe.":
            "countries of coverage — from Lubumbashi to Windhoek, via Lusaka and Lilongwe.",
        "Pays couverts": "Countries covered",
        "Ancrage local": "Local roots",
        "Les valeurs qui guident notre équipe": "The values that guide our team",
        "Proximité": "Closeness",
        "Des agents présents physiquement dans chaque pays, pas seulement une application.":
            "Agents physically present in every country, not just an app.",
        "Écoute": "Listening",
        "Chaque client a une situation différente ; notre équipe prend le temps de comprendre.":
            "Every customer's situation is different; our team takes the time to understand.",
        "Réactivité": "Responsiveness",
        "Des réponses rapides sur WhatsApp et par téléphone, y compris en dehors des heures classiques.":
            "Fast responses on WhatsApp and by phone, even outside regular hours.",
        "Engagement": "Commitment",
        "Une équipe impliquée dans les communautés qu'elle sert, au-delà des transactions.":
            "A team invested in the communities it serves, beyond the transactions.",
        "Une équipe portée par sa communauté": "A team carried by its community",
        "Au-delà des bureaux et des agences, Blue Sky c'est aussi les personnes qui portent fièrement nos couleurs au quotidien — collègues, proches et membres de la communauté qui nous font confiance.":
            "Beyond the offices and branches, Blue Sky is also the people who proudly wear our colors every day — colleagues, loved ones, and community members who trust us.",

        # --- impact ---
        "Connecter les familles, soutenir les communautés": "Connecting families, supporting communities",
        "Le métier de Blue Sky est de rapprocher les familles séparées par la distance. Nous croyons fermement que cette mission ne s'arrête pas aux transactions financières.":
            "Blue Sky's business is bringing together families separated by distance. We firmly believe this mission doesn't stop at financial transactions.",
        "Aux côtés d'un orphelinat en Namibie": "Alongside an orphanage in Namibia",
        "L'équipe Blue Sky se déplace régulièrement auprès d'enfants d'un orphelinat en Namibie pour partager du temps, apporter des ressources et rester à l'écoute de leurs besoins au quotidien.":
            "The Blue Sky team regularly visits children at an orphanage in Namibia to share time, bring resources, and stay attentive to their day-to-day needs.",
        "Ces visites font partie intégrante de l'ADN de Blue Sky : une entreprise africaine, construite par et pour ses communautés. Une partie de notre présence locale dans chaque pays sert ainsi à identifier des initiatives à fort impact que nous pouvons soutenir dans la durée.":
            "These visits are part of Blue Sky's DNA: an African company, built by and for its communities. Part of our local presence in every country is about identifying high-impact initiatives we can support over the long run.",
        "Engagements récurrents": "Ongoing commitments",
        "Action locale en Namibie": "Local action in Namibia",
        "Proximité & Entraide": "Closeness & mutual support",
        "Créer un impact tangible au-delà des frontières.": "Creating a tangible impact beyond borders.",
        "Grandir aux côtés de la jeunesse africaine": "Growing alongside African youth",
        "Soutenir l'éducation et la réussite des jeunes fait partie de notre engagement — parce qu'investir dans une génération, c'est investir dans l'avenir des familles que nous connectons chaque jour.":
            "Supporting young people's education and success is part of our commitment — because investing in a generation means investing in the future of the families we connect every day.",
        "Votre argent fait avancer ce qui compte vraiment": "Your money moves what truly matters",
        "Un transfert ne se résume pas à un montant. C'est un repas partagé, un diplôme qui se rapproche ou une idée qui devient une vraie activité.":
            "A transfer isn't just an amount. It's a shared meal, a diploma within reach, or an idea becoming a real business.",
        "Toujours proche des siens": "Always close to your own",
        "Contribuer au quotidien, aux soins et aux projets de la famille, même lorsque des frontières vous séparent.":
            "Contributing to daily life, care, and family projects, even when borders separate you.",
        "Soutenir le quotidien": "Support day-to-day life",
        "Investir dans leur avenir": "Investing in their future",
        "Payer les frais de scolarité, le logement ou le matériel nécessaire pour apprendre et réussir sereinement.":
            "Paying school fees, housing, or the equipment needed to learn and succeed with peace of mind.",
        "Financer les études": "Fund education",
        "Entrepreneurs": "Entrepreneurs",
        "Donner de l'élan aux idées": "Giving ideas momentum",
        "Acheter du matériel, payer un fournisseur ou renforcer la trésorerie pour transformer une ambition en activité durable.":
            "Buying equipment, paying a supplier, or strengthening cash flow to turn an ambition into a lasting business.",
        "Faire grandir l'activité": "Grow the business",
        "Préparez vos projets avec confiance": "Prepare your projects with confidence",
        "Une épargne simple, régulière et adaptée à vos ambitions": "Savings that are simple, regular, and suited to your ambitions",
        "Études, projet familial ou développement d'activité : avancez à votre rythme avec un accompagnement humain et un suivi transparent.":
            "Studies, a family project, or growing a business: move at your own pace with human support and transparent tracking.",
        "Branche Blue Sky": "Blue Sky branch",
        "Découvrir l'épargne": "Discover Savings",
        "Sur le terrain": "On the ground",
        "Un engagement soutenu aux côtés des acteurs locaux": "A sustained commitment alongside local partners",
        "Vous connaissez une initiative locale à soutenir ?": "Know a local initiative worth supporting?",
        "Parlez-nous de votre communauté — nous sommes toujours à l'écoute de nouvelles façons de nous rendre utiles là où nous opérons.":
            "Tell us about your community — we're always open to new ways to be useful wherever we operate.",

        # --- contact ---
        "Parlons de votre prochain transfert": "Let's talk about your next transfer",
        "Une question, un projet ou besoin d'aide ? Écrivez-nous : un membre de notre équipe vous accompagne personnellement.":
            "A question, a project, or need a hand? Write to us: a member of our team will personally assist you.",
        "Vous vous enrôlez pour le service Épargne": "You're signing up for the Savings service",
        "Nous sommes à votre écoute": "We're here to listen",
        "Choisissez le canal qui vous convient. Notre équipe répond avec attention et vous guide à chaque étape.":
            "Choose whichever channel suits you. Our team responds attentively and guides you every step of the way.",
        "Siège social": "Head office",
        "E-mail": "Email",
        "Réponse rapide": "Fast reply",
        "Écrivez-nous sur WhatsApp": "Write to us on WhatsApp",
        "Disponible du lundi au samedi, de 08h00 à 18h00": "Available Monday to Saturday, 08:00–18:00",
        "Message envoyé": "Message sent",
        "Merci de nous avoir contactés. Notre équipe vous répondra très prochainement.":
            "Thank you for contacting us. Our team will get back to you very soon.",
        "Envoyez votre demande": "Send your request",
        "Comment pouvons-nous vous aider ?": "How can we help you?",
        "Remplissez ce formulaire et nous vous répondrons dans les meilleurs délais.":
            "Fill out this form and we'll get back to you as soon as possible.",
        "Envoyer le message": "Send message",
        "Vos informations restent confidentielles et servent uniquement à vous répondre.":
            "Your information stays confidential and is only used to reply to you.",
        "Siège social · Lubumbashi": "Head office · Lubumbashi",
        "En face de l'Hôtel Hypnose": "Across from Hôtel Hypnose",
        "Obtenir l'itinéraire": "Get directions",
        "Une équipe joignable, une communauté fidèle": "A team you can reach, a loyal community",
        "Que ce soit par téléphone, WhatsApp ou en agence, notre équipe reste à l'écoute — merci à toutes les personnes qui portent fièrement les couleurs Blue Sky partout où elles se trouvent.":
            "Whether by phone, WhatsApp, or in branch, our team stays attentive — thank you to everyone who proudly wears Blue Sky's colors wherever they are.",

        # --- countries page ---
        "Plus proches de vous, dans": "Closer to you, in",
        "Retrouvez les adresses et contacts de nos agences. Dans les pays en développement de réseau, vos opérations sont assurées par transfert électronique avec l'accompagnement direct de notre équipe.":
            "Find the addresses and contacts of our branches. In countries where our network is still developing, your transactions are handled by electronic transfer with direct support from our team.",
        "Agence physique": "Physical branch",
        "Transfert électronique accompagné": "Supported electronic transfer",

        # --- kickers (auto-translated wherever {% kicker %} is used) ---
        "Qui sommes-nous ?": "Who we are",
        "Notre vision": "Our vision",
        "L'équipe Blue Sky": "The Blue Sky team",
        "Ce qui nous anime": "What drives us",
        "Responsabilité sociale": "Social responsibility",
        "Ce que permet chaque transfert": "What every transfer makes possible",
        "Notre réseau africain": "Our African network",
        "Parlons-en": "Let's talk",

        # --- blog ---
        "Les dernières nouvelles de Blue Sky": "The latest news from Blue Sky",
        "Lire la suite": "Read more",
        "Précédent": "Previous",
        "Page": "Page",
        "Suivant": "Next",
        "Aucune actualité publiée pour le moment.": "No news published yet.",
        "Toutes les actualités": "All news",
        "Brouillon — visible uniquement par le personnel": "Draft — visible to staff only",
        "Non publié": "Not published",
    },
    # Machine-checked but not proofread by a native Kiswahili speaker — good
    # enough to launch with, but worth a native-speaker pass before this is
    # the language East African customers rely on day to day.
    "sw": {
        # --- header / nav ---
        "Accueil": "Nyumbani",
        "À propos": "Kuhusu",
        "Équipe": "Timu",
        "Actualités": "Habari",
        "Nos pays": "Nchi zetu",
        "Épargne": "Akiba",
        "Lun–Sam : 08h00–18h00": "Jumatatu–Jumamosi: Saa 08:00–18:00",
        "Basculer le mode sombre": "Badilisha hali ya giza",
        "Nous contacter": "Wasiliana nasi",

        # --- footer ---
        "Blue Sky / Afrique australe": "Blue Sky / Kusini mwa Afrika",
        "L'argent voyage.": "Pesa husafiri.",
        "La confiance reste.": "Uaminifu unabaki.",
        "Notre équipe": "Timu yetu",
        "Notre impact": "Athari yetu",
        "Nos agences": "Matawi yetu",
        "Contact direct": "Mawasiliano ya moja kwa moja",
        "Tous droits réservés.": "Haki zote zimehifadhiwa.",
        "Présent dans": "Tupo katika",
        "pays": "nchi",

        # --- country names (shared across footer, cards, forms) ---
        "Congo (RDC)": "DR Congo",
        "Zambie": "Zambia",
        "Namibie": "Namibia",
        "Afrique du Sud": "Afrika Kusini",
        "Tanzanie": "Tanzania",
        "Ouganda": "Uganda",

        # --- country cards ---
        "Drapeau de": "Bendera ya",
        "Agence": "Tawi",
        "Transfert digital": "Uhamishaji wa kidijitali",
        "Adresse & contacts": "Anwani na mawasiliano",
        "Adresse de l'agence": "Anwani ya tawi",
        "Service de transfert électronique": "Huduma ya uhamishaji wa kielektroniki",
        "Effectuez vos opérations à distance avec l'accompagnement direct de notre équipe. Un point d'accueil physique sera annoncé prochainement.":
            "Fanya shughuli zako kwa mbali ukiwa na msaada wa moja kwa moja kutoka kwa timu yetu. Eneo la ofisi litatangazwa hivi karibuni.",
        "Téléphone & WhatsApp": "Simu na WhatsApp",
        "Airtel Money & MTN Money disponibles sur place": "Airtel Money na MTN Money zinapatikana papo hapo",
        "Envoyez de l'argent au Kenya facilement, rapidement et en toute sécurité.":
            "Tuma pesa nchini Kenya kwa urahisi, haraka na kwa usalama.",
        "Nouvelle agence": "Tawi jipya",

        # --- homepage: hero ---
        "Le transfert qui nous rapproche": "Uhamishaji unaotuleta karibu zaidi",
        'Envoyez plus loin.<br><span class="text-brand-blue">Restez plus proche.</span>':
            'Tuma mbali zaidi.<br><span class="text-brand-blue">Baki karibu zaidi.</span>',
        "Envoyez de l'argent dans": "Tuma pesa katika",
        "pays africains avec un suivi transparent, un accompagnement humain et la sérénité à chaque étape.":
            "nchi za Afrika ukiwa na ufuatiliaji wazi, msaada wa kibinadamu na utulivu katika kila hatua.",
        "Parler à un conseiller": "Zungumza na mshauri",
        "Un accompagnement humain": "Msaada wa kibinadamu",
        "avant, pendant et après chaque transfert": "kabla, wakati na baada ya kila uhamishaji",
        "Données protégées": "Data zilizolindwa",
        "Transfert suivi": "Uhamishaji unaofuatiliwa",
        "Support humain": "Msaada wa kibinadamu",
        "Envoyer de l'argent": "Kutuma pesa",
        "Vous envoyez": "Unatuma",
        "Demander un devis": "Omba bei",

        # --- homepage: construction CTA ---
        'Construisez votre avenir en toute <span class="text-brand-gold">sécurité</span> et en toute <span class="text-brand-gold">confiance</span> avec Blue Sky':
            'Jenga maisha yako ya baadaye kwa <span class="text-brand-gold">usalama</span> kamili na <span class="text-brand-gold">imani</span> kamili na Blue Sky',
        "Qu'il s'agisse de financer un projet de construction, de soutenir votre famille ou de faire grandir votre activité, Blue Sky vous accompagne dans":
            "Iwe unafadhili mradi wa ujenzi, kusaidia familia yako au kukuza biashara yako, Blue Sky inakusaidia katika",
        "pays d'Afrique avec la même rigueur à chaque transfert.": "nchi za Afrika kwa umakini uleule katika kila uhamishaji.",
        "Nous contacter pour ce service": "Wasiliana nasi kwa huduma hii",

        # --- homepage: services ---
        "Bâtissons ensemble": "Tujenge pamoja",
        "Pourquoi Blue Sky": "Kwa nini Blue Sky",
        "Des services construits autour de la confiance": "Huduma zilizojengwa kwa msingi wa imani",
        "Une présence locale, un suivi transparent et une équipe disponible pour que chaque transfert reste simple du départ à l'arrivée.":
            "Uwepo wa karibu, ufuatiliaji wazi na timu iliyo tayari kuhakikisha kila uhamishaji unabaki rahisi kutoka mwanzo hadi mwisho.",
        "Découvrir": "Gundua",
        "100% sécurisé": "Salama 100%",
        "Chaque transaction est protégée et suivie de bout en bout, sans mauvaise surprise.":
            "Kila muamala unalindwa na kufuatiliwa mwanzo hadi mwisho, bila mshangao mbaya.",
        "Ultra rapide": "Haraka sana",
        "Vos bénéficiaires reçoivent leurs fonds en quelques minutes, pas en quelques jours.":
            "Wanufaika wako wanapokea fedha zao ndani ya dakika chache, si siku kadhaa.",
        "Réseau régional": "Mtandao wa kikanda",
        "9 pays d'Afrique australe et de l'Est connectés à une seule plateforme.":
            "Nchi 9 za Kusini na Mashariki mwa Afrika zilizounganishwa kwenye jukwaa moja.",
        "Assistance humaine": "Msaada wa kibinadamu",
        "Une équipe joignable sur WhatsApp et par téléphone, dans chaque pays où nous opérons.":
            "Timu inayopatikana kupitia WhatsApp na simu, katika kila nchi tunayofanya kazi.",

        # --- homepage: steps ---
        "Comment ça marche": "Jinsi inavyofanya kazi",
        "Trois étapes pour envoyer votre premier transfert": "Hatua tatu za kutuma uhamishaji wako wa kwanza",
        "Étape": "Hatua",
        "Créez votre compte": "Fungua akaunti yako",
        "Inscription en quelques minutes pour accéder à votre tableau de bord Blue Sky.":
            "Jisajili ndani ya dakika chache ili kufikia dashibodi yako ya Blue Sky.",
        "Ajoutez un bénéficiaire": "Ongeza mnufaika",
        "Enregistrez les informations de la personne qui recevra les fonds.":
            "Hifadhi taarifa za mtu atakayepokea fedha.",
        "Envoyez en toute confiance": "Tuma kwa uhakika kamili",
        "Choisissez le montant et le moyen de paiement, nous nous occupons du reste.":
            "Chagua kiasi na njia ya malipo, sisi tunashughulikia mengine.",

        # --- homepage: countries + partners ---
        "Notre couverture": "Ufikiaji wetu",
        "Nos agences à travers l'Afrique": "Matawi yetu kote Afrika",
        "Moyens de paiement &amp; partenaires mobiles": "Njia za malipo na washirika wa simu",

        # --- homepage: savings ---
        "Épargner un peu, chaque mois": "Weka akiba kidogo kila mwezi",
        "Notre branche Épargne": "Tawi letu la Akiba",
        "Épargnez sereinement, à votre rythme": "Weka akiba kwa utulivu, kwa kasi yako",
        (
            "En plus du transfert d'argent, Blue Sky propose une branche Épargne : "
            "un moyen simple et sécurisé de mettre de l'argent de côté pour vos études, "
            "votre famille ou votre activité. Vous êtes enregistré dans notre programme "
            "d'épargne et vous pouvez suivre votre compte à tout moment, avec le même "
            "accompagnement humain qu'en agence."
        ): (
            "Mbali na uhamishaji wa pesa, Blue Sky inatoa huduma ya Akiba: njia rahisi na "
            "salama ya kuweka pesa kando kwa ajili ya masomo yako, familia yako au biashara "
            "yako. Unasajiliwa katika programu yetu ya akiba na unaweza kufuatilia akaunti "
            "yako wakati wowote, ukiwa na msaada uleule wa kibinadamu kama tawini."
        ),
        "Étudiants": "Wanafunzi",
        "Mettez de côté pour vos frais académiques et vos projets d'avenir, à votre rythme.":
            "Weka pesa kando kwa ajili ya ada zako za masomo na mipango yako ya baadaye, kwa kasi yako.",
        "Familles": "Familia",
        "Construisez un fonds commun pour les imprévus, les études des enfants ou un projet familial.":
            "Jenga akiba ya pamoja kwa ajili ya dharura, masomo ya watoto au mradi wa familia.",
        "Entreprises": "Biashara",
        "Épargnez pour votre fonds de roulement ou vos investissements, avec un suivi dédié.":
            "Weka akiba kwa ajili ya mtaji wa kufanyia kazi au uwekezaji wako, ukiwa na ufuatiliaji maalum.",
        "S'enrôler au service épargne": "Jiunge na huduma ya Akiba",
        "Ou écrivez-nous directement sur": "Au tuandikie moja kwa moja kupitia",

        # --- homepage: hero stats ---
        "pays connectés": "nchi zilizounganishwa",
        "moyens de paiement": "njia za malipo",
        "suivi personnalisé": "ufuatiliaji binafsi",
        "équipe à votre écoute": "timu iliyo tayari kukusikiliza",

        # --- homepage: community / impact ---
        "pays reliés par une même équipe": "nchi zilizounganishwa na timu moja",
        "Au-delà du transfert d'argent": "Zaidi ya uhamishaji wa pesa",
        "Une expertise locale, portée par des relations humaines": "Utaalamu wa karibu, unaoendeshwa na mahusiano ya kibinadamu",
        (
            "L'équipe Blue Sky se rend régulièrement auprès d'enfants d'un orphelinat en "
            "Namibie pour offrir du temps, des ressources et du soutien — parce que "
            "connecter les familles va au-delà des transactions."
        ): (
            "Timu ya Blue Sky hutembelea mara kwa mara watoto wa kituo cha malezi nchini "
            "Namibia ili kutoa muda, rasilimali na msaada — kwa sababu kuunganisha familia "
            "huenda zaidi ya miamala."
        ),
        "Présence locale": "Uwepo wa karibu",
        "Des équipes sur le terrain, pas seulement en ligne.": "Timu zilizopo uwandani, si mtandaoni tu.",
        "Impact direct": "Athari ya moja kwa moja",
        "Du temps et des ressources pour les communautés locales.": "Muda na rasilimali kwa ajili ya jamii za karibu.",
        "Engagement communautaire": "Ushirikiano wa kijamii",
        "Découvrir notre impact": "Gundua athari yetu",

        # --- homepage: final CTA ---
        "Commencez aujourd'hui": "Anza leo",
        "Prêt à envoyer votre argent en toute confiance ?": "Uko tayari kutuma pesa yako kwa uhakika kamili?",
        "Contactez l'équipe Blue Sky ou rendez-vous dans l'agence la plus proche pour démarrer votre transfert.":
            "Wasiliana na timu ya Blue Sky au tembelea tawi lililo karibu nawe ili kuanza uhamishaji wako.",
        "Appelez-nous": "Tupigie simu",
        "Nous écrire": "Tuandikie",
        "Trouver une agence": "Tafuta tawi",

        # --- shared form fields/errors ---
        "Nom complet": "Jina kamili",
        "Entrez votre nom complet": "Weka jina lako kamili",
        "Adresse e-mail": "Anwani ya barua pepe",
        "Adresse e-mail invalide": "Anwani ya barua pepe si sahihi",
        "Téléphone": "Simu",
        "Numéro de téléphone invalide": "Nambari ya simu si sahihi",
        "Pays": "Nchi",
        "Sélectionnez votre pays": "Chagua nchi yako",
        "Mot de passe": "Nenosiri",
        "Le mot de passe doit contenir au moins 8 caractères": "Nenosiri lazima liwe na angalau herufi 8",
        "Un compte existe déjà avec cette adresse e-mail.": "Akaunti tayari ipo kwa anwani hii ya barua pepe.",
        "Adresse e-mail déjà utilisée": "Anwani ya barua pepe tayari inatumika",
        "Adresse e-mail ou mot de passe invalide.": "Anwani ya barua pepe au nenosiri si sahihi.",
        "Merci de corriger les champs indiqués.": "Tafadhali sahihisha sehemu zilizoainishwa.",
        "Sujet de votre demande": "Somo la ombi lako",
        "Votre message": "Ujumbe wako",
        "Votre message est un peu court": "Ujumbe wako ni mfupi kidogo",

        # --- auth ---
        "Un réseau. Huit pays.": "Mtandao mmoja. Nchi nane.",
        'L\'argent arrive.<br>La confiance aussi.': 'Pesa inafika.<br>Uaminifu pia.',
        "Connexion": "Ingia",
        "Accédez à votre tableau de bord Blue Sky.": "Fikia dashibodi yako ya Blue Sky.",
        "Se connecter": "Ingia",
        "Pas encore de compte ?": "Huna akaunti bado?",
        "Ouvrir un compte": "Fungua akaunti",
        "Quelques minutes suffisent": "Dakika chache zinatosha",
        'Notez vos infos.<br>On s\'occupe du reste.': 'Andika taarifa zako.<br>Sisi tunashughulikia mengine.',
        "Créez votre compte Blue Sky en quelques minutes.": "Fungua akaunti yako ya Blue Sky ndani ya dakika chache.",
        "Créer mon compte": "Fungua akaunti yangu",
        "Déjà un compte ?": "Una akaunti tayari?",

        # --- about ---
        "Une agence bâtie pour rapprocher les familles africaines": "Wakala uliojengwa kuunganisha familia za Afrika",
        "Notre but": "Lengo letu",
        "Notre mission": "Dhamira yetu",
        "L'équipe de direction, Blue Sky": "Uongozi wa Blue Sky",
        "Cette vision guide chacune de nos décisions : ouvrir de nouvelles agences là où les familles en ont besoin, simplifier chaque étape du transfert, et rester joignables humainement, pas seulement via une application.":
            "Dira hii inaongoza kila uamuzi wetu: kufungua matawi mapya pale familia zinapohitaji, kurahisisha kila hatua ya uhamishaji, na kubaki tunapatikana kibinadamu, si kupitia programu tu.",
        "&laquo; Nous voulons qu'aucune distance, aucune frontière n'empêche une famille de prendre soin des siens. Blue Sky existe pour que chaque franc, chaque kwacha, chaque rand envoyé arrive à destination avec la même confiance qu'une remise en main propre. &raquo;":
            "&laquo; Tunataka umbali wowote, mpaka wowote usizuie familia kutunza wapendwa wao. Blue Sky ipo ili kila faranga, kila kwacha, kila randi iliyotumwa ifike na uaminifu uleule kama kukabidhiwa mkononi. &raquo;",
        (
            "Blue Sky est une agence de transfert d'argent spécialisée dans les "
            "transactions internationales entre la République Démocratique du Congo, la "
            "Namibie, la Zambie, l'Afrique du Sud, le Zimbabwe, le Kenya, l'Ouganda, la "
            "Tanzanie et le Malawi. Nous offrons des solutions rapides, fiables et "
            "sécurisées pour envoyer et recevoir de l'argent à travers ces pays."
        ): (
            "Blue Sky ni wakala wa uhamishaji wa pesa uliobobea katika miamala ya "
            "kimataifa kati ya Jamhuri ya Kidemokrasia ya Kongo, Namibia, Zambia, Afrika "
            "Kusini, Zimbabwe, Kenya, Uganda, Tanzania na Malawi. Tunatoa suluhisho la "
            "haraka, la kuaminika na salama la kutuma na kupokea pesa katika nchi hizi."
        ),
        (
            "Faciliter l'envoi et la réception d'argent à l'international en garantissant "
            "la rapidité et l'efficacité."
        ): (
            "Kurahisisha utumaji na upokeaji wa pesa kimataifa kwa kuhakikisha kasi na "
            "ufanisi."
        ),

        # --- team ---
        "Des visages humains derrière vos transferts": "Nyuso za kibinadamu nyuma ya uhamishaji wako",
        "Derrière chaque transfert Blue Sky, une équipe ancrée en Afrique australe veille chaque jour à ce que votre argent arrive vite et en toute sécurité.":
            "Nyuma ya kila uhamishaji wa Blue Sky, timu iliyoko Kusini mwa Afrika inahakikisha kila siku pesa yako inafika haraka na kwa usalama.",
        "Proximité & Terrain": "Ukaribu na Uwandani",
        "Une présence locale forte dans chaque agence.": "Uwepo dhabiti wa karibu katika kila tawi.",
        "Notre équipe combine des profils opérationnels, un service client réactif et des agents locaux répartis dans nos":
            "Timu yetu inajumuisha wataalamu wa uendeshaji, huduma kwa wateja inayowajibika kwa haraka na mawakala wa karibu waliosambaa katika",
        "de couverture — de Lubumbashi à Windhoek, en passant par Lusaka et Lilongwe.":
            "nchi zetu za ufikiaji — kutoka Lubumbashi hadi Windhoek, kupitia Lusaka na Lilongwe.",
        "Pays couverts": "Nchi zinazofikiwa",
        "Ancrage local": "Mizizi ya karibu",
        "Les valeurs qui guident notre équipe": "Maadili yanayoongoza timu yetu",
        "Proximité": "Ukaribu",
        "Des agents présents physiquement dans chaque pays, pas seulement une application.":
            "Mawakala waliopo kimwili katika kila nchi, si programu tu.",
        "Écoute": "Kusikiliza",
        "Chaque client a une situation différente ; notre équipe prend le temps de comprendre.":
            "Kila mteja ana hali tofauti; timu yetu inachukua muda kuelewa.",
        "Réactivité": "Ufanisi wa haraka",
        "Des réponses rapides sur WhatsApp et par téléphone, y compris en dehors des heures classiques.":
            "Majibu ya haraka kupitia WhatsApp na simu, hata nje ya saa za kawaida.",
        "Engagement": "Kujitolea",
        "Une équipe impliquée dans les communautés qu'elle sert, au-delà des transactions.":
            "Timu inayojishughulisha na jamii inazohudumia, zaidi ya miamala.",
        "Une équipe portée par sa communauté": "Timu inayoungwa mkono na jamii yake",
        "Au-delà des bureaux et des agences, Blue Sky c'est aussi les personnes qui portent fièrement nos couleurs au quotidien — collègues, proches et membres de la communauté qui nous font confiance.":
            "Zaidi ya ofisi na matawi, Blue Sky pia ni watu wanaovaa rangi zetu kwa fahari kila siku — wenzetu, wapendwa na wanajamii wanaotuamini.",

        # --- impact ---
        "Connecter les familles, soutenir les communautés": "Kuunganisha familia, kusaidia jamii",
        "Le métier de Blue Sky est de rapprocher les familles séparées par la distance. Nous croyons fermement que cette mission ne s'arrête pas aux transactions financières.":
            "Kazi ya Blue Sky ni kuunganisha familia zilizotenganishwa na umbali. Tunaamini kwa dhati kuwa dhamira hii haiishii kwenye miamala ya kifedha.",
        "Aux côtés d'un orphelinat en Namibie": "Bega kwa bega na kituo cha malezi nchini Namibia",
        "L'équipe Blue Sky se déplace régulièrement auprès d'enfants d'un orphelinat en Namibie pour partager du temps, apporter des ressources et rester à l'écoute de leurs besoins au quotidien.":
            "Timu ya Blue Sky hutembelea mara kwa mara watoto wa kituo cha malezi nchini Namibia kutoa muda, kuleta rasilimali na kubaki makini kwa mahitaji yao ya kila siku.",
        "Ces visites font partie intégrante de l'ADN de Blue Sky : une entreprise africaine, construite par et pour ses communautés. Une partie de notre présence locale dans chaque pays sert ainsi à identifier des initiatives à fort impact que nous pouvons soutenir dans la durée.":
            "Ziara hizi ni sehemu muhimu ya tabia ya Blue Sky: kampuni ya Kiafrika, iliyojengwa na jamii zake kwa ajili yao. Sehemu ya uwepo wetu wa karibu katika kila nchi hutumika kutambua mipango yenye athari kubwa tunayoweza kuisaidia kwa muda mrefu.",
        "Engagements récurrents": "Ahadi za kudumu",
        "Action locale en Namibie": "Hatua za karibu nchini Namibia",
        "Proximité & Entraide": "Ukaribu na Msaada",
        "Créer un impact tangible au-delà des frontières.": "Kuleta athari halisi zaidi ya mipaka.",
        "Grandir aux côtés de la jeunesse africaine": "Kukua bega kwa bega na vijana wa Afrika",
        "Soutenir l'éducation et la réussite des jeunes fait partie de notre engagement — parce qu'investir dans une génération, c'est investir dans l'avenir des familles que nous connectons chaque jour.":
            "Kusaidia elimu na mafanikio ya vijana ni sehemu ya ahadi yetu — kwa sababu kuwekeza kwa kizazi ni kuwekeza katika maisha ya baadaye ya familia tunazounganisha kila siku.",
        "Votre argent fait avancer ce qui compte vraiment": "Pesa yako inasukuma mbele kile kinachostahili",
        "Un transfert ne se résume pas à un montant. C'est un repas partagé, un diplôme qui se rapproche ou une idée qui devient une vraie activité.":
            "Uhamishaji si kiasi tu. Ni mlo unaoshirikiwa, shahada inayokaribia au wazo linalogeuka kuwa biashara halisi.",
        "Toujours proche des siens": "Daima karibu na wapendwa",
        "Contribuer au quotidien, aux soins et aux projets de la famille, même lorsque des frontières vous séparent.":
            "Kuchangia maisha ya kila siku, matunzo na mipango ya familia, hata pale mipaka inapowatenganisha.",
        "Soutenir le quotidien": "Saidia maisha ya kila siku",
        "Investir dans leur avenir": "Kuwekeza katika maisha yao ya baadaye",
        "Payer les frais de scolarité, le logement ou le matériel nécessaire pour apprendre et réussir sereinement.":
            "Kulipa ada za masomo, malazi au vifaa muhimu ili kujifunza na kufaulu kwa utulivu.",
        "Financer les études": "Fadhili masomo",
        "Entrepreneurs": "Wajasiriamali",
        "Donner de l'élan aux idées": "Kuipa nguvu mawazo",
        "Acheter du matériel, payer un fournisseur ou renforcer la trésorerie pour transformer une ambition en activité durable.":
            "Kununua vifaa, kulipa muuzaji au kuimarisha mtaji ili kugeuza azma kuwa biashara endelevu.",
        "Faire grandir l'activité": "Kukuza biashara",
        "Préparez vos projets avec confiance": "Andaa mipango yako kwa uhakika",
        "Une épargne simple, régulière et adaptée à vos ambitions": "Akiba rahisi, ya kudumu na inayolingana na malengo yako",
        "Études, projet familial ou développement d'activité : avancez à votre rythme avec un accompagnement humain et un suivi transparent.":
            "Masomo, mradi wa familia au ukuaji wa biashara: songa mbele kwa kasi yako ukiwa na msaada wa kibinadamu na ufuatiliaji wazi.",
        "Branche Blue Sky": "Tawi la Blue Sky",
        "Découvrir l'épargne": "Gundua huduma ya Akiba",
        "Sur le terrain": "Uwandani",
        "Un engagement soutenu aux côtés des acteurs locaux": "Ahadi endelevu bega kwa bega na wadau wa karibu",
        "Vous connaissez une initiative locale à soutenir ?": "Unajua mpango wa karibu unaostahili kuungwa mkono?",
        "Parlez-nous de votre communauté — nous sommes toujours à l'écoute de nouvelles façons de nous rendre utiles là où nous opérons.":
            "Tuambie kuhusu jamii yako — daima tuko tayari kusikia njia mpya za kuwa na manufaa popote tunapofanya kazi.",

        # --- contact ---
        "Parlons de votre prochain transfert": "Tuzungumze kuhusu uhamishaji wako ujao",
        "Une question, un projet ou besoin d'aide ? Écrivez-nous : un membre de notre équipe vous accompagne personnellement.":
            "Una swali, mradi au unahitaji msaada? Tuandikie: mwanachama wa timu yetu atakusaidia binafsi.",
        "Vous vous enrôlez pour le service Épargne": "Unajiunga na huduma ya Akiba",
        "Nous sommes à votre écoute": "Tuko tayari kukusikiliza",
        "Choisissez le canal qui vous convient. Notre équipe répond avec attention et vous guide à chaque étape.":
            "Chagua njia inayokufaa. Timu yetu inajibu kwa makini na kukuongoza katika kila hatua.",
        "Siège social": "Makao makuu",
        "E-mail": "Barua pepe",
        "Réponse rapide": "Jibu la haraka",
        "Écrivez-nous sur WhatsApp": "Tuandikie kupitia WhatsApp",
        "Disponible du lundi au samedi, de 08h00 à 18h00": "Tunapatikana Jumatatu hadi Jumamosi, saa 08:00–18:00",
        "Message envoyé": "Ujumbe umetumwa",
        "Merci de nous avoir contactés. Notre équipe vous répondra très prochainement.":
            "Asante kwa kuwasiliana nasi. Timu yetu itakujibu hivi karibuni.",
        "Envoyez votre demande": "Tuma ombi lako",
        "Comment pouvons-nous vous aider ?": "Tunawezaje kukusaidia?",
        "Remplissez ce formulaire et nous vous répondrons dans les meilleurs délais.":
            "Jaza fomu hii na tutakujibu haraka iwezekanavyo.",
        "Envoyer le message": "Tuma ujumbe",
        "Vos informations restent confidentielles et servent uniquement à vous répondre.":
            "Taarifa zako zinabaki siri na zinatumika tu kukujibu.",
        "Siège social · Lubumbashi": "Makao makuu · Lubumbashi",
        "En face de l'Hôtel Hypnose": "Mkabala na Hôtel Hypnose",
        "Obtenir l'itinéraire": "Pata mwelekeo",
        "Une équipe joignable, une communauté fidèle": "Timu inayofikika, jamii thabiti",
        "Que ce soit par téléphone, WhatsApp ou en agence, notre équipe reste à l'écoute — merci à toutes les personnes qui portent fièrement les couleurs Blue Sky partout où elles se trouvent.":
            "Iwe kwa simu, WhatsApp au tawi, timu yetu inabaki makini — asante kwa kila mtu anayevaa rangi za Blue Sky kwa fahari popote alipo.",

        # --- countries page ---
        "Plus proches de vous, dans": "Karibu zaidi na wewe, katika",
        "Retrouvez les adresses et contacts de nos agences. Dans les pays en développement de réseau, vos opérations sont assurées par transfert électronique avec l'accompagnement direct de notre équipe.":
            "Pata anwani na mawasiliano ya matawi yetu. Katika nchi ambazo mtandao bado unaendelea kukua, shughuli zako zinafanywa kwa uhamishaji wa kielektroniki ukiwa na msaada wa moja kwa moja kutoka kwa timu yetu.",
        "Agence physique": "Tawi la kimwili",
        "Transfert électronique accompagné": "Uhamishaji wa kielektroniki unaosaidiwa",

        # --- kickers ---
        "Qui sommes-nous ?": "Sisi ni akina nani?",
        "Notre vision": "Dira yetu",
        "L'équipe Blue Sky": "Timu ya Blue Sky",
        "Ce qui nous anime": "Kinachotusukuma",
        "Responsabilité sociale": "Uwajibikaji wa kijamii",
        "Ce que permet chaque transfert": "Kile kila uhamishaji kinachowezesha",
        "Notre réseau africain": "Mtandao wetu wa Afrika",
        "Parlons-en": "Tuzungumze",

        # --- blog ---
        "Les dernières nouvelles de Blue Sky": "Habari za hivi karibuni za Blue Sky",
        "Lire la suite": "Soma zaidi",
        "Précédent": "Iliyotangulia",
        "Page": "Ukurasa",
        "Suivant": "Ifuatayo",
        "Aucune actualité publiée pour le moment.": "Hakuna habari iliyochapishwa kwa sasa.",
        "Toutes les actualités": "Habari zote",
        "Brouillon — visible uniquement par le personnel": "Rasimu — inaonekana kwa wafanyakazi tu",
        "Non publié": "Haijachapishwa",
    },
}
