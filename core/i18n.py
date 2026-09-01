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
        "Tarifs": "Rates",
        "Informations de paiement": "Payment information",
        "Épargne": "Savings",
        "Lundi au samedi : 08h00 à 18h00": "Monday to Saturday: 08:00 to 18:00",
        "Basculer le mode sombre": "Toggle dark mode",
        "Nous contacter": "Contact us",
        "Tableau de bord": "Dashboard",
        "Mon compte": "My account",

        # --- tariffs ---
        "Consultez les tarifs d'envoi et de retrait Blue Sky.": "View Blue Sky transfer and withdrawal rates.",
        "Des tarifs simples et transparents": "Simple, transparent rates",
        "Consultez les frais applicables à vos envois et retraits avant chaque transaction.": "Check the fees for transfers and withdrawals before each transaction.",
        "Dernière mise à jour": "Last updated",
        "Envoi": "Transfer",
        "Retrait": "Withdrawal",
        "Envoi vers la Tanzanie": "Transfer to Tanzania",
        "Depuis les autres pays Blue Sky vers la Tanzanie": "From other Blue Sky countries to Tanzania",
        "Retrait hors Tanzanie": "Withdrawal outside Tanzania",
        "Envoi hors Tanzanie": "Transfer outside Tanzania",
        "Tous les pays Blue Sky sauf la Tanzanie": "All Blue Sky countries except Tanzania",
        "Montant": "Amount",
        "Frais": "Fee",
        "À partir de": "From",
        "Envoyez de l'argent en toute sécurité": "Send money securely",
        "L'argent voyage en toute sécurité": "Money travels securely",
        "Tarifs en cours de mise à jour": "Rates are being updated",
        "Contactez notre équipe pour connaître les frais applicables à votre transaction.": "Contact our team to confirm the fees for your transaction.",
        "Les frais affichés sont indicatifs et peuvent être actualisés. Le tarif applicable vous sera confirmé avant la validation de votre transaction.": "Displayed fees are indicative and may be updated. Your applicable rate will be confirmed before the transaction is approved.",
        "Information importante": "Important information",
        "Les tarifs peuvent évoluer. Avant toute opération, veuillez toujours contacter un conseiller Blue Sky afin de vérifier les frais actuellement en vigueur. Le montant définitif vous sera confirmé avant la validation de votre transaction.": "Rates may change. Before any transaction, always contact a Blue Sky adviser to confirm the fees currently in effect. The final amount will be confirmed before your transaction is approved.",
        "Besoin d'aide ?": "Need help?",
        "Préparez votre prochain transfert avec nous": "Plan your next transfer with us",
        "Notre équipe vous confirme le tarif, le délai et le point de retrait le plus proche.": "Our team will confirm the rate, timing and nearest pickup point.",
        "Tarif spécial Tanzanie": "Special Tanzania rate",
        "Transferts envoyés vers ou depuis la Tanzanie": "Transfers sent to or from Tanzania",
        "Tarif retrait quotidien": "Daily withdrawal rate",
        "Tarif envoi quotidien": "Daily transfer rate",
        "Tarif standard du réseau Blue Sky": "Standard Blue Sky network rate",
        "Particularité Tanzanie : les transferts envoyés vers ou depuis la Tanzanie bénéficient d'une grille tarifaire différente des tarifs quotidiens.": "Tanzania special rate: transfers sent to or from Tanzania use a different rate schedule from the daily rates.",
        "Espace client sécurisé": "Secure customer area",
        "Utilisez exclusivement les coordonnées confirmées dans votre espace Blue Sky. Ces informations sont réservées aux clients connectés.": "Only use details confirmed in your Blue Sky account. This information is reserved for signed-in customers.",
        "Vérification obligatoire": "Mandatory verification",
        "Avant tout dépôt ou retrait, contactez toujours un conseiller Blue Sky afin de confirmer le numéro, le titulaire et les instructions en vigueur. N'effectuez aucune opération vers des coordonnées reçues en dehors des canaux officiels Blue Sky.": "Before any deposit or withdrawal, always contact a Blue Sky adviser to confirm the number, account holder and current instructions. Never transact using details received outside official Blue Sky channels.",
        "Mis à jour le": "Updated on",
        "Aucun compte de paiement n'est actuellement disponible.": "No payment account is currently available.",
        "Retrait cash à": "Cash pickup in",
        "Aucune information de paiement n'est actuellement disponible.": "No payment information is currently available.",

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
        "Voir l'adresse et les contacts": "View address and contacts",
        "Voir les coordonnées pour": "View contact details for",
        "Coordonnées": "Contact details",
        "Fermer": "Close",
        "Agences locales": "Local branches",
        "Gros plan du drapeau de la RDC": "Close-up of the DR Congo flag",
        "Gros plan du drapeau de l'Afrique du Sud": "Close-up of the South African flag",
        "Gros plan du drapeau de l'Ouganda": "Close-up of the Ugandan flag",
        "Gros plan du drapeau de la Namibie": "Close-up of the Namibian flag",

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
        "L'Afrique n'a jamais été aussi proche": "Africa has never felt this close",
        'Votre argent voyage.<br><span class="text-brand-sky">Vos liens restent.</span>':
            'Your money travels.<br><span class="text-brand-sky">Your connections remain.</span>',
        "Des transferts fiables, suivis et accompagnés par de vraies personnes dans":
            "Reliable, tracked transfers supported by real people across",
        "pays africains.": "African countries.",
        "Démarrer un transfert": "Start a transfer",
        "Voir notre réseau": "View our network",
        "Estimation rapide": "Quick estimate",
        "Simple. Clair. Accompagné.": "Simple. Clear. Supported.",
        "vers l'Afrique": "to Africa",
        "Transferts suivis": "Tracked transfers",
        "pays desservis": "countries served",
        "Menu": "Menu",
        "Blue Sky en chiffres": "Blue Sky in numbers",
        "Moyens de paiement et partenaires mobiles": "Payment methods and mobile partners",
        "Page introuvable": "Page not found",
        "Blue Sky, transfert d'argent international": "Blue Sky, international money transfer",
        "Blue Sky connecte la RDC, la Zambie, la Namibie, l'Afrique du Sud, le Zimbabwe, le Kenya, l'Ouganda, la Tanzanie et le Malawi pour des transferts d'argent rapides, fiables et sécurisés.":
            "Blue Sky connects DR Congo, Zambia, Namibia, South Africa, Zimbabwe, Kenya, Uganda, Tanzania, and Malawi for fast, reliable, and secure money transfers.",

        # --- homepage: construction CTA ---
        'Construisez votre avenir en toute <span class="text-brand-sky">sécurité</span> et en toute <span class="text-brand-sky">confiance</span> avec Blue Sky':
            'Build your future in complete <span class="text-brand-sky">safety</span> and <span class="text-brand-sky">confidence</span> with Blue Sky',
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
        "pays d'Afrique australe et de l'Est connectés à une seule plateforme.":
            "African countries across Southern and East Africa connected on one platform.",
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
            "Namibie pour offrir du temps, des ressources et du soutien, parce que "
            "connecter les familles va au-delà des transactions."
        ): (
            "The Blue Sky team regularly visits children at an orphanage in Namibia to "
            "offer time, resources, and support, because connecting families goes beyond "
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
        "Confirmer le mot de passe": "Confirm password",
        "Confirmez votre mot de passe": "Confirm your password",
        "Les mots de passe ne correspondent pas.": "Passwords do not match.",
        "Code de vérification": "Verification code",
        "Entrez le code à 6 chiffres": "Enter the 6-digit code",
        "Le mot de passe doit contenir au moins 8 caractères": "Password must be at least 8 characters",
        "Un compte existe déjà avec cette adresse e-mail.": "An account already exists with this email address.",
        "Adresse e-mail déjà utilisée": "Email address already in use",
        "Adresse e-mail ou mot de passe invalide.": "Invalid email address or password.",
        "Adresse e-mail ou mot de passe incorrect.": "Incorrect email address or password.",
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
        "Vérifier votre e-mail": "Verify your email",
        "Vérifiez votre e-mail": "Check your email",
        "Sécurité du compte": "Account security",
        'Un dernier geste.<br>Votre compte est prêt.': 'One last step.<br>Your account is ready.',
        "Nous avons envoyé un code à 6 chiffres à": "We sent a 6-digit code to",
        "Le code expire dans 10 minutes.": "The code expires in 10 minutes.",
        "Vérifier et continuer": "Verify and continue",
        "Renvoyer le code": "Resend code",
        "Vous pourrez demander un nouveau code après 60 secondes.": "You can request a new code after 60 seconds.",
        "Ce code a expiré. Demandez un nouveau code.": "This code has expired. Request a new one.",
        "Code incorrect. Vérifiez puis réessayez.": "Incorrect code. Check it and try again.",

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
        "de couverture, de Lubumbashi à Windhoek, en passant par Lusaka et Lilongwe.":
            "countries of coverage, from Lubumbashi to Windhoek, via Lusaka and Lilongwe.",
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
        "Au-delà des bureaux et des agences, Blue Sky c'est aussi les personnes qui portent fièrement nos couleurs au quotidien : collègues, proches et membres de la communauté qui nous font confiance.":
            "Beyond the offices and branches, Blue Sky is also the people who proudly wear our colors every day: colleagues, loved ones, and community members who trust us.",

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
        "Soutenir l'éducation et la réussite des jeunes fait partie de notre engagement, parce qu'investir dans une génération, c'est investir dans l'avenir des familles que nous connectons chaque jour.":
            "Supporting young people's education and success is part of our commitment, because investing in a generation means investing in the future of the families we connect every day.",
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
        "Parlez-nous de votre communauté. Nous sommes toujours à l'écoute de nouvelles façons de nous rendre utiles là où nous opérons.":
            "Tell us about your community. We are always open to new ways to be useful wherever we operate.",

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
        "Disponible du lundi au samedi, de 08h00 à 18h00": "Available Monday to Saturday, from 08:00 to 18:00",
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
        "Que ce soit par téléphone, WhatsApp ou en agence, notre équipe reste à l'écoute. Merci à toutes les personnes qui portent fièrement les couleurs Blue Sky partout où elles se trouvent.":
            "Whether by phone, WhatsApp, or in branch, our team stays attentive. Thank you to everyone who proudly wears Blue Sky's colors wherever they are.",

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
        "Brouillon, visible uniquement par le personnel": "Draft, visible to staff only",
        "Non publié": "Not published",

        # --- misc gaps closed on a translation audit pass ---
        "Fierté locale": "Local pride",
        "Contact": "Contact",
        "Changer de langue": "Change language",
        "Carte du siège social Blue Sky à Lubumbashi": "Map of Blue Sky's head office in Lubumbashi",

        # --- 404 ---
        "Erreur 404": "Error 404",
        "Cette page n'existe pas": "This page doesn't exist",
        "La page que vous cherchez a peut-être été déplacée ou n'existe plus.":
            "The page you're looking for may have moved or no longer exists.",
        "Retour à l'accueil": "Back to home",

        # --- dashboard chrome (transfers/savings) ---
        "Se déconnecter": "Log out",
        "Vue d'ensemble": "Overview",
        "Bénéficiaires": "Recipients",
        "Nouveau transfert": "New transfer",

        # --- transfers dashboard ---
        "Bonjour": "Hello",
        "Voici un aperçu de votre activité Blue Sky.": "Here's an overview of your Blue Sky activity.",
        "Transferts récents": "Recent transfers",
        "Ajouter un bénéficiaire": "Add a recipient",
        "Vous n'avez encore effectué aucun transfert.": "You haven't made any transfers yet.",
        "Envoyer mon premier transfert": "Send my first transfer",
        "Référence": "Reference",
        "Destination": "Destination",
        "Montant": "Amount",
        "Statut": "Status",
        "Date": "Date",
        "Annuler": "Cancel",
        "Transferts envoyés": "Transfers sent",
        "En attente": "Pending",
        "Terminés": "Completed",
        "Renseignez les détails de votre envoi. Notre équipe vous contactera pour la confirmation.":
            "Enter your transfer details. Our team will contact you to confirm.",
        "Ajoutez d'abord un bénéficiaire avant d'envoyer un transfert.": "Add a recipient first before sending a transfer.",
        "Envoyer la demande de transfert": "Send transfer request",
        "Votre demande sera confirmée par notre équipe avant traitement.": "Your request will be confirmed by our team before processing.",
        "Gérez les personnes qui reçoivent vos transferts.": "Manage the people who receive your transfers.",
        "Ajouter le bénéficiaire": "Add recipient",
        "Aucun bénéficiaire enregistré pour le moment.": "No recipients registered yet.",
        "Supprimer": "Delete",

        # --- savings dashboard ---
        "Notez vos infos, on s'occupe du reste.": "Jot down your details, we'll take it from there.",
        "Ouvrir un compte épargne": "Open a savings account",
        "Remplissez ces quelques informations pour soumettre votre demande. Notre équipe activera votre compte après vérification.":
            "Fill in these few details to submit your request. Our team will activate your account after verification.",
        "Soumettre ma demande": "Submit my request",
        "Mon épargne": "My savings",
        "Fiche": "Record",
        "Votre demande est en cours de vérification": "Your request is under review",
        "Solde disponible": "Available balance",
        "Total déposé": "Total deposited",
        "Total retiré": "Total withdrawn",
        "Demander une opération": "Request an operation",
        "Chaque dépôt ou retrait doit être confirmé par notre équipe avant de mettre à jour votre solde.":
            "Every deposit or withdrawal is confirmed by our team before your balance is updated.",
        "Envoyer la demande": "Send request",
        "Votre compte n'est pas encore actif. Vous pourrez demander un dépôt ou un retrait une fois qu'il sera activé par notre équipe.":
            "Your account is not active yet. You will be able to request a deposit or withdrawal once our team activates it.",
        "Type": "Type",
        "Nouveau solde": "New balance",
        "Aucune opération pour le moment.": "No operations yet.",

        # --- model status/type labels (savings + transfers) ---
        "En attente d'activation": "Awaiting activation",
        "Actif": "Active",
        "Refusé": "Rejected",
        "Clôturé": "Closed",
        "Dépôt": "Deposit",
        "Retrait": "Withdrawal",
        "Confirmé": "Confirmed",
        "Rejeté": "Rejected",
        "En cours": "Processing",
        "Terminé": "Completed",
        "Annulé": "Cancelled",

        # --- contact form service choices ---
        "Transfert d'argent": "Money transfer",
        "Autre": "Other",

        # --- dashboard form labels/errors ---
        "Nom du bénéficiaire requis": "Recipient name required",
        "Sélectionnez un pays": "Select a country",
        "Autre pays": "Other country",
        "Navigation": "Navigation",

        # --- alt text closed on a translation audit pass ---
        "Portrait de la direction de Blue Sky": "Portrait of Blue Sky's leadership",
        "Un membre de la communauté Blue Sky portant un t-shirt à l'effigie de la marque":
            "A member of the Blue Sky community wearing a branded t-shirt",
        "L'équipe Blue Sky sur le terrain": "The Blue Sky team in the field",
        "Pièces empilées symbolisant la croissance de l'épargne": "Stacked coins symbolizing savings growth",
        "Blue Sky aux côtés des enfants d'un orphelinat en Namibie":
            "Blue Sky alongside children at an orphanage in Namibia",
        "Une membre de l'équipe Blue Sky avec une enfant de l'orphelinat":
            "A Blue Sky team member with a child from the orphanage",
        "Une étudiante soutenue par la communauté Blue Sky portant un t-shirt à l'effigie de la marque":
            "A student supported by the Blue Sky community wearing a branded t-shirt",
        "Une famille africaine épargnant ensemble à la maison": "An African family saving together at home",
        "Une étudiante avec ses cahiers, soutenue par sa famille via Blue Sky":
            "A student with her notebooks, supported by her family via Blue Sky",
        "Une jeune entrepreneure africaine au téléphone devant son commerce":
            "A young African entrepreneur on the phone outside her shop",
        "L'équipe Blue Sky entourée des enfants de l'orphelinat lors d'une visite":
            "The Blue Sky team surrounded by children from the orphanage during a visit",
        "L'équipe Blue Sky réunie sur le terrain": "The Blue Sky team gathered in the field",
        "Deux membres de la communauté Blue Sky portant des t-shirts à l'effigie de la marque":
            "Two members of the Blue Sky community wearing branded t-shirts",
        "Téléphone (optionnel)": "Phone (optional)",
        "Relation (optionnel)": "Relationship (optional)",
        "Bénéficiaire": "Recipient",
        "Le montant doit être supérieur à 0": "Amount must be greater than 0",
        "Devise": "Currency",
        "Moyen de paiement": "Payment method",
        "Sélectionnez un moyen de paiement": "Select a payment method",
        "Note (optionnel)": "Note (optional)",
        "Type d'opération": "Operation type",
        "Observations (optionnel)": "Comments (optional)",
        "N° CNI / Passeport": "ID / passport number",
        "Entrez votre numéro de CNI ou passeport": "Enter your ID or passport number",
        "Adresse": "Address",
        "Entrez votre adresse": "Enter your address",
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
        "Tarifs": "Viwango",
        "Informations de paiement": "Taarifa za malipo",
        "Épargne": "Akiba",
        "Lundi au samedi : 08h00 à 18h00": "Jumatatu hadi Jumamosi: Saa 08:00 hadi 18:00",
        "Basculer le mode sombre": "Badilisha hali ya giza",
        "Nous contacter": "Wasiliana nasi",
        "Tableau de bord": "Dashibodi",
        "Mon compte": "Akaunti yangu",

        # --- tariffs ---
        "Consultez les tarifs d'envoi et de retrait Blue Sky.": "Angalia viwango vya kutuma na kutoa pesa vya Blue Sky.",
        "Des tarifs simples et transparents": "Viwango rahisi na vya uwazi",
        "Consultez les frais applicables à vos envois et retraits avant chaque transaction.": "Angalia ada za kutuma na kutoa pesa kabla ya kila muamala.",
        "Dernière mise à jour": "Ilisasishwa mwisho",
        "Envoi": "Kutuma",
        "Retrait": "Kutoa",
        "Envoi vers la Tanzanie": "Kutuma pesa kwenda Tanzania",
        "Depuis les autres pays Blue Sky vers la Tanzanie": "Kutoka nchi nyingine za Blue Sky kwenda Tanzania",
        "Retrait hors Tanzanie": "Kutoa pesa nje ya Tanzania",
        "Envoi hors Tanzanie": "Kutuma pesa nje ya Tanzania",
        "Tous les pays Blue Sky sauf la Tanzanie": "Nchi zote za Blue Sky isipokuwa Tanzania",
        "Montant": "Kiasi",
        "Frais": "Ada",
        "À partir de": "Kuanzia",
        "Envoyez de l'argent en toute sécurité": "Tuma pesa kwa usalama",
        "L'argent voyage en toute sécurité": "Pesa husafiri kwa usalama",
        "Tarifs en cours de mise à jour": "Viwango vinasasishwa",
        "Contactez notre équipe pour connaître les frais applicables à votre transaction.": "Wasiliana na timu yetu kuthibitisha ada za muamala wako.",
        "Les frais affichés sont indicatifs et peuvent être actualisés. Le tarif applicable vous sera confirmé avant la validation de votre transaction.": "Ada zilizoonyeshwa ni za mwongozo na zinaweza kusasishwa. Kiwango chako kitathibitishwa kabla ya muamala kuidhinishwa.",
        "Information importante": "Taarifa muhimu",
        "Les tarifs peuvent évoluer. Avant toute opération, veuillez toujours contacter un conseiller Blue Sky afin de vérifier les frais actuellement en vigueur. Le montant définitif vous sera confirmé avant la validation de votre transaction.": "Viwango vinaweza kubadilika. Kabla ya muamala wowote, wasiliana kila wakati na mshauri wa Blue Sky ili kuthibitisha ada zinazotumika kwa sasa. Kiasi cha mwisho kitathibitishwa kabla ya muamala wako kuidhinishwa.",
        "Besoin d'aide ?": "Unahitaji msaada?",
        "Préparez votre prochain transfert avec nous": "Panga uhamisho wako ujao nasi",
        "Notre équipe vous confirme le tarif, le délai et le point de retrait le plus proche.": "Timu yetu itathibitisha kiwango, muda na sehemu ya karibu ya kuchukua pesa.",
        "Tarif spécial Tanzanie": "Kiwango maalum cha Tanzania",
        "Transferts envoyés vers ou depuis la Tanzanie": "Uhamisho unaotumwa kwenda au kutoka Tanzania",
        "Tarif retrait quotidien": "Kiwango cha kila siku cha kutoa pesa",
        "Tarif envoi quotidien": "Kiwango cha kila siku cha kutuma pesa",
        "Tarif standard du réseau Blue Sky": "Kiwango cha kawaida cha mtandao wa Blue Sky",
        "Particularité Tanzanie : les transferts envoyés vers ou depuis la Tanzanie bénéficient d'une grille tarifaire différente des tarifs quotidiens.": "Kiwango maalum cha Tanzania: uhamisho unaotumwa kwenda au kutoka Tanzania hutumia viwango tofauti na viwango vya kila siku.",
        "Espace client sécurisé": "Eneo salama la mteja",
        "Utilisez exclusivement les coordonnées confirmées dans votre espace Blue Sky. Ces informations sont réservées aux clients connectés.": "Tumia taarifa zilizothibitishwa katika akaunti yako ya Blue Sky pekee. Taarifa hizi ni za wateja walioingia kwenye akaunti.",
        "Vérification obligatoire": "Uthibitishaji wa lazima",
        "Avant tout dépôt ou retrait, contactez toujours un conseiller Blue Sky afin de confirmer le numéro, le titulaire et les instructions en vigueur. N'effectuez aucune opération vers des coordonnées reçues en dehors des canaux officiels Blue Sky.": "Kabla ya kuweka au kutoa pesa, wasiliana kila wakati na mshauri wa Blue Sky kuthibitisha namba, jina la mwenye akaunti na maelekezo ya sasa. Usifanye muamala kwa taarifa zilizopokelewa nje ya njia rasmi za Blue Sky.",
        "Mis à jour le": "Ilisasishwa tarehe",
        "Aucun compte de paiement n'est actuellement disponible.": "Hakuna akaunti ya malipo inayopatikana kwa sasa.",
        "Retrait cash à": "Kuchukua pesa taslimu mjini",
        "Aucune information de paiement n'est actuellement disponible.": "Hakuna taarifa za malipo zinazopatikana kwa sasa.",

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
        "Voir l'adresse et les contacts": "Tazama anwani na mawasiliano",
        "Voir les coordonnées pour": "Tazama mawasiliano ya",
        "Coordonnées": "Maelezo ya mawasiliano",
        "Fermer": "Funga",
        "Agences locales": "Matawi ya karibu",
        "Gros plan du drapeau de la RDC": "Picha ya karibu ya bendera ya DR Congo",
        "Gros plan du drapeau de l'Afrique du Sud": "Picha ya karibu ya bendera ya Afrika Kusini",
        "Gros plan du drapeau de l'Ouganda": "Picha ya karibu ya bendera ya Uganda",
        "Gros plan du drapeau de la Namibie": "Picha ya karibu ya bendera ya Namibia",

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
        "L'Afrique n'a jamais été aussi proche": "Afrika haijawahi kuwa karibu hivi",
        'Votre argent voyage.<br><span class="text-brand-sky">Vos liens restent.</span>':
            'Pesa yako inasafiri.<br><span class="text-brand-sky">Mahusiano yako yanadumu.</span>',
        "Des transferts fiables, suivis et accompagnés par de vraies personnes dans":
            "Uhamishaji wa kuaminika, unaofuatiliwa na kusaidiwa na watu halisi katika",
        "pays africains.": "nchi za Afrika.",
        "Démarrer un transfert": "Anza uhamishaji",
        "Voir notre réseau": "Tazama mtandao wetu",
        "Estimation rapide": "Makadirio ya haraka",
        "Simple. Clair. Accompagné.": "Rahisi. Wazi. Unaosaidiwa.",
        "vers l'Afrique": "kwenda Afrika",
        "Transferts suivis": "Uhamishaji unaofuatiliwa",
        "pays desservis": "nchi zinazohudumiwa",
        "Menu": "Menyu",
        "Blue Sky en chiffres": "Blue Sky kwa takwimu",
        "Moyens de paiement et partenaires mobiles": "Njia za malipo na washirika wa simu",
        "Page introuvable": "Ukurasa haujapatikana",
        "Blue Sky, transfert d'argent international": "Blue Sky, uhamishaji wa pesa kimataifa",
        "Blue Sky connecte la RDC, la Zambie, la Namibie, l'Afrique du Sud, le Zimbabwe, le Kenya, l'Ouganda, la Tanzanie et le Malawi pour des transferts d'argent rapides, fiables et sécurisés.":
            "Blue Sky inaunganisha DR Congo, Zambia, Namibia, Afrika Kusini, Zimbabwe, Kenya, Uganda, Tanzania na Malawi kwa uhamishaji wa pesa wa haraka, wa kuaminika na salama.",

        # --- homepage: construction CTA ---
        'Construisez votre avenir en toute <span class="text-brand-sky">sécurité</span> et en toute <span class="text-brand-sky">confiance</span> avec Blue Sky':
            'Jenga maisha yako ya baadaye kwa <span class="text-brand-sky">usalama</span> kamili na <span class="text-brand-sky">imani</span> kamili na Blue Sky',
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
        "pays d'Afrique australe et de l'Est connectés à une seule plateforme.":
            "nchi za Kusini na Mashariki mwa Afrika zilizounganishwa kwenye jukwaa moja.",
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
            "Namibie pour offrir du temps, des ressources et du soutien, parce que "
            "connecter les familles va au-delà des transactions."
        ): (
            "Timu ya Blue Sky hutembelea mara kwa mara watoto wa kituo cha malezi nchini "
            "Namibia ili kutoa muda, rasilimali na msaada, kwa sababu kuunganisha familia "
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
        "Confirmer le mot de passe": "Thibitisha nenosiri",
        "Confirmez votre mot de passe": "Thibitisha nenosiri lako",
        "Les mots de passe ne correspondent pas.": "Manenosiri hayalingani.",
        "Code de vérification": "Nambari ya uthibitishaji",
        "Entrez le code à 6 chiffres": "Weka nambari yenye tarakimu 6",
        "Le mot de passe doit contenir au moins 8 caractères": "Nenosiri lazima liwe na angalau herufi 8",
        "Un compte existe déjà avec cette adresse e-mail.": "Akaunti tayari ipo kwa anwani hii ya barua pepe.",
        "Adresse e-mail déjà utilisée": "Anwani ya barua pepe tayari inatumika",
        "Adresse e-mail ou mot de passe invalide.": "Anwani ya barua pepe au nenosiri si sahihi.",
        "Adresse e-mail ou mot de passe incorrect.": "Anwani ya barua pepe au nenosiri si sahihi.",
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
        "Vérifier votre e-mail": "Thibitisha barua pepe yako",
        "Vérifiez votre e-mail": "Angalia barua pepe yako",
        "Sécurité du compte": "Usalama wa akaunti",
        'Un dernier geste.<br>Votre compte est prêt.': 'Hatua moja ya mwisho.<br>Akaunti yako iko tayari.',
        "Nous avons envoyé un code à 6 chiffres à": "Tumetuma nambari yenye tarakimu 6 kwa",
        "Le code expire dans 10 minutes.": "Nambari itaisha baada ya dakika 10.",
        "Vérifier et continuer": "Thibitisha na uendelee",
        "Renvoyer le code": "Tuma nambari tena",
        "Vous pourrez demander un nouveau code après 60 secondes.": "Unaweza kuomba nambari mpya baada ya sekunde 60.",
        "Ce code a expiré. Demandez un nouveau code.": "Nambari hii imekwisha muda. Omba nambari mpya.",
        "Code incorrect. Vérifiez puis réessayez.": "Nambari si sahihi. Iangalie kisha ujaribu tena.",

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
        "de couverture, de Lubumbashi à Windhoek, en passant par Lusaka et Lilongwe.":
            "nchi zetu za ufikiaji, kutoka Lubumbashi hadi Windhoek, kupitia Lusaka na Lilongwe.",
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
        "Au-delà des bureaux et des agences, Blue Sky c'est aussi les personnes qui portent fièrement nos couleurs au quotidien : collègues, proches et membres de la communauté qui nous font confiance.":
            "Zaidi ya ofisi na matawi, Blue Sky pia ni watu wanaovaa rangi zetu kwa fahari kila siku: wenzetu, wapendwa na wanajamii wanaotuamini.",

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
        "Soutenir l'éducation et la réussite des jeunes fait partie de notre engagement, parce qu'investir dans une génération, c'est investir dans l'avenir des familles que nous connectons chaque jour.":
            "Kusaidia elimu na mafanikio ya vijana ni sehemu ya ahadi yetu, kwa sababu kuwekeza kwa kizazi ni kuwekeza katika maisha ya baadaye ya familia tunazounganisha kila siku.",
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
        "Parlez-nous de votre communauté. Nous sommes toujours à l'écoute de nouvelles façons de nous rendre utiles là où nous opérons.":
            "Tuambie kuhusu jamii yako. Daima tuko tayari kusikia njia mpya za kuwa na manufaa popote tunapofanya kazi.",

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
        "Disponible du lundi au samedi, de 08h00 à 18h00": "Tunapatikana Jumatatu hadi Jumamosi, kuanzia saa 08:00 hadi 18:00",
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
        "Que ce soit par téléphone, WhatsApp ou en agence, notre équipe reste à l'écoute. Merci à toutes les personnes qui portent fièrement les couleurs Blue Sky partout où elles se trouvent.":
            "Iwe kwa simu, WhatsApp au tawi, timu yetu inabaki makini. Asante kwa kila mtu anayevaa rangi za Blue Sky kwa fahari popote alipo.",

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
        "Brouillon, visible uniquement par le personnel": "Rasimu, inaonekana kwa wafanyakazi tu",
        "Non publié": "Haijachapishwa",

        # --- misc gaps closed on a translation audit pass ---
        "Fierté locale": "Fahari ya karibu",
        "Contact": "Mawasiliano",
        "Changer de langue": "Badilisha lugha",
        "Carte du siège social Blue Sky à Lubumbashi": "Ramani ya makao makuu ya Blue Sky mjini Lubumbashi",

        # --- 404 ---
        "Erreur 404": "Hitilafu 404",
        "Cette page n'existe pas": "Ukurasa huu haupo",
        "La page que vous cherchez a peut-être été déplacée ou n'existe plus.":
            "Ukurasa unaoutafuta huenda ulihamishwa au haupo tena.",
        "Retour à l'accueil": "Rudi mwanzoni",

        # --- dashboard chrome (transfers/savings) ---
        "Se déconnecter": "Toka",
        "Vue d'ensemble": "Muhtasari",
        "Bénéficiaires": "Wanufaika",
        "Nouveau transfert": "Uhamishaji mpya",

        # --- transfers dashboard ---
        "Bonjour": "Habari",
        "Voici un aperçu de votre activité Blue Sky.": "Huu ni muhtasari wa shughuli zako za Blue Sky.",
        "Transferts récents": "Uhamishaji wa hivi karibuni",
        "Ajouter un bénéficiaire": "Ongeza mnufaika",
        "Vous n'avez encore effectué aucun transfert.": "Bado hujafanya uhamishaji wowote.",
        "Envoyer mon premier transfert": "Tuma uhamishaji wangu wa kwanza",
        "Référence": "Kumbukumbu",
        "Destination": "Mwelekeo",
        "Montant": "Kiasi",
        "Statut": "Hali",
        "Date": "Tarehe",
        "Annuler": "Ghairi",
        "Transferts envoyés": "Uhamishaji uliotumwa",
        "En attente": "Inasubiri",
        "Terminés": "Zilizokamilika",
        "Renseignez les détails de votre envoi. Notre équipe vous contactera pour la confirmation.":
            "Jaza maelezo ya utumaji wako. Timu yetu itawasiliana nawe kuthibitisha.",
        "Ajoutez d'abord un bénéficiaire avant d'envoyer un transfert.": "Ongeza mnufaika kwanza kabla ya kutuma uhamishaji.",
        "Envoyer la demande de transfert": "Tuma ombi la uhamishaji",
        "Votre demande sera confirmée par notre équipe avant traitement.": "Ombi lako litathibitishwa na timu yetu kabla ya kushughulikiwa.",
        "Gérez les personnes qui reçoivent vos transferts.": "Simamia watu wanaopokea uhamishaji wako.",
        "Ajouter le bénéficiaire": "Ongeza mnufaika",
        "Aucun bénéficiaire enregistré pour le moment.": "Hakuna mnufaika aliyesajiliwa kwa sasa.",
        "Supprimer": "Futa",

        # --- savings dashboard ---
        "Notez vos infos, on s'occupe du reste.": "Andika taarifa zako, sisi tunashughulikia mengine.",
        "Ouvrir un compte épargne": "Fungua akaunti ya akiba",
        "Remplissez ces quelques informations pour soumettre votre demande. Notre équipe activera votre compte après vérification.":
            "Jaza taarifa hizi chache kuwasilisha ombi lako. Timu yetu itawasha akaunti yako baada ya uhakiki.",
        "Soumettre ma demande": "Wasilisha ombi langu",
        "Mon épargne": "Akiba yangu",
        "Fiche": "Rekodi",
        "Votre demande est en cours de vérification": "Ombi lako liko katika hatua ya uhakiki",
        "Solde disponible": "Salio linalopatikana",
        "Total déposé": "Jumla iliyowekwa",
        "Total retiré": "Jumla iliyotolewa",
        "Demander une opération": "Omba shughuli",
        "Chaque dépôt ou retrait doit être confirmé par notre équipe avant de mettre à jour votre solde.":
            "Kila uwekaji au utoaji lazima uthibitishwe na timu yetu kabla ya salio lako kusasishwa.",
        "Envoyer la demande": "Tuma ombi",
        "Votre compte n'est pas encore actif. Vous pourrez demander un dépôt ou un retrait une fois qu'il sera activé par notre équipe.":
            "Akaunti yako bado haijawashwa. Utaweza kuomba uwekaji au utoaji mara timu yetu itakapoiwasha.",
        "Type": "Aina",
        "Nouveau solde": "Salio jipya",
        "Aucune opération pour le moment.": "Hakuna shughuli kwa sasa.",

        # --- model status/type labels (savings + transfers) ---
        "En attente d'activation": "Inasubiri kuwashwa",
        "Actif": "Hai",
        "Refusé": "Imekataliwa",
        "Clôturé": "Imefungwa",
        "Dépôt": "Uwekaji",
        "Retrait": "Utoaji",
        "Confirmé": "Imethibitishwa",
        "Rejeté": "Imekataliwa",
        "En cours": "Inaendelea",
        "Terminé": "Imekamilika",
        "Annulé": "Imeghairiwa",

        # --- contact form service choices ---
        "Transfert d'argent": "Uhamishaji wa pesa",
        "Autre": "Nyingine",

        # --- dashboard form labels/errors ---
        "Nom du bénéficiaire requis": "Jina la mnufaika linahitajika",
        "Sélectionnez un pays": "Chagua nchi",
        "Autre pays": "Nchi nyingine",
        "Navigation": "Urambazaji",

        # --- alt text closed on a translation audit pass ---
        "Portrait de la direction de Blue Sky": "Picha ya uongozi wa Blue Sky",
        "Un membre de la communauté Blue Sky portant un t-shirt à l'effigie de la marque":
            "Mwanajamii wa Blue Sky akiwa amevaa t-shirt yenye nembo ya chapa",
        "L'équipe Blue Sky sur le terrain": "Timu ya Blue Sky uwandani",
        "Pièces empilées symbolisant la croissance de l'épargne": "Sarafu zilizopangwa zinazoashiria ukuaji wa akiba",
        "Blue Sky aux côtés des enfants d'un orphelinat en Namibie":
            "Blue Sky bega kwa bega na watoto wa kituo cha malezi nchini Namibia",
        "Une membre de l'équipe Blue Sky avec une enfant de l'orphelinat":
            "Mwanachama wa timu ya Blue Sky na mtoto wa kituo cha malezi",
        "Une étudiante soutenue par la communauté Blue Sky portant un t-shirt à l'effigie de la marque":
            "Mwanafunzi anayeungwa mkono na jamii ya Blue Sky akiwa amevaa t-shirt yenye nembo ya chapa",
        "Une famille africaine épargnant ensemble à la maison": "Familia ya Kiafrika ikiweka akiba pamoja nyumbani",
        "Une étudiante avec ses cahiers, soutenue par sa famille via Blue Sky":
            "Mwanafunzi na daftari zake, akiungwa mkono na familia yake kupitia Blue Sky",
        "Une jeune entrepreneure africaine au téléphone devant son commerce":
            "Mjasiriamali kijana wa Kiafrika akiwa kwenye simu mbele ya duka lake",
        "L'équipe Blue Sky entourée des enfants de l'orphelinat lors d'une visite":
            "Timu ya Blue Sky ikizungukwa na watoto wa kituo cha malezi wakati wa ziara",
        "L'équipe Blue Sky réunie sur le terrain": "Timu ya Blue Sky ikiwa pamoja uwandani",
        "Deux membres de la communauté Blue Sky portant des t-shirts à l'effigie de la marque":
            "Wanajamii wawili wa Blue Sky wakiwa wamevaa t-shirt zenye nembo ya chapa",
        "Téléphone (optionnel)": "Simu (hiari)",
        "Relation (optionnel)": "Uhusiano (hiari)",
        "Bénéficiaire": "Mnufaika",
        "Le montant doit être supérieur à 0": "Kiasi lazima kiwe zaidi ya 0",
        "Devise": "Sarafu",
        "Moyen de paiement": "Njia ya malipo",
        "Sélectionnez un moyen de paiement": "Chagua njia ya malipo",
        "Note (optionnel)": "Maelezo (hiari)",
        "Type d'opération": "Aina ya shughuli",
        "Observations (optionnel)": "Maoni (hiari)",
        "N° CNI / Passeport": "Nambari ya kitambulisho / Pasipoti",
        "Entrez votre numéro de CNI ou passeport": "Weka nambari yako ya kitambulisho au pasipoti",
        "Adresse": "Anwani",
        "Entrez votre adresse": "Weka anwani yako",
    },
}


def translate(text, lang):
    """Translate a single string for the given language code — the same
    lookup `{% t %}` performs in templates, exposed for Python code (form
    `choices=` built outside a template) that needs it directly."""
    if lang == SOURCE_LANGUAGE:
        return text
    return TRANSLATIONS.get(lang, {}).get(text, text)


def translated_choices(choices, lang):
    """Translate the labels of a Django choices iterable for the given
    language code, leaving the stored values untouched.

    `choices` is an iterable of (value, label) pairs — what a
    forms.ChoiceField(choices=...) or a model TextChoices class accepts.
    Falls back to the French label when no translation exists yet, exactly
    like `{% t %}`. Use this for form field `choices=` where the option
    text is real copy (e.g. country names, operation types) rather than a
    brand name or currency code that shouldn't be translated.
    """
    if lang == SOURCE_LANGUAGE:
        return list(choices)
    table = TRANSLATIONS.get(lang, {})
    return [(value, table.get(label, label)) for value, label in choices]
