from django.db import migrations, models


AGENCIES = [
    ("CD", "Congo (RDC)", "🇨🇩", "Avenue Kapenda, Coins Mobutu, en face de l'Hôtel Hypnose, Quartier Makutano, Commune de Lubumbashi, Haut-Katanga", "+243 972 113 974\n+243 989 555 229", ""),
    ("ZM", "Zambie", "🇿🇲", "Inter City Bus Station", "+260 771 306 147\n+260 974 909 125\n+260 773 144 727", "Airtel Money & MTN Money disponibles sur place"),
    ("NA", "Namibie", "🇳🇦", "3 Weber Street, Windhoek, près de l'entrée principale de NUST", "+264 857 681 484", ""),
    ("ZA", "Afrique du Sud", "🇿🇦", "", "+243 972 113 974", ""),
    ("TZ", "Tanzanie", "🇹🇿", "Marché Kariakoo", "+255 745 157 262", ""),
    ("KE", "Kenya", "🇰🇪", "", "+254 117 194 191", "Envoyez de l'argent au Kenya facilement, rapidement et en toute sécurité."),
    ("UG", "Ouganda", "🇺🇬", "Kampala", "+243 972 113 974", "Nouvelle agence"),
    ("ZW", "Zimbabwe", "🇿🇼", "Africa University, Mutare", "+243 974 344 310", ""),
    ("MW", "Malawi", "🇲🇼", "Lilongwe, Area 47 / Secteur 3 No. 15", "+265 992 040 049", ""),
]


def seed_agencies(apps, schema_editor):
    Agency = apps.get_model("marketing", "Agency")
    Agency.objects.bulk_create([
        Agency(code=code, country_name=name, flag=flag, address=address,
               phone_numbers=phones, note=note, display_order=order)
        for order, (code, name, flag, address, phones, note) in enumerate(AGENCIES, start=1)
    ])


class Migration(migrations.Migration):
    dependencies = [("marketing", "0005_paymentlocation_paymentaccount")]
    operations = [
        migrations.CreateModel(
            name="Agency",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=2, unique=True, verbose_name="Code pays")),
                ("country_name", models.CharField(max_length=100, verbose_name="Pays")),
                ("flag", models.CharField(blank=True, max_length=10, verbose_name="Drapeau")),
                ("address", models.TextField(blank=True, verbose_name="Adresse de l'agence")),
                ("phone_numbers", models.TextField(blank=True, help_text="Saisissez un numéro par ligne.", verbose_name="Numéros de téléphone")),
                ("note", models.TextField(blank=True, verbose_name="Note")),
                ("is_active", models.BooleanField(default=True, verbose_name="Visible sur le site")),
                ("display_order", models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Dernière modification")),
            ],
            options={"verbose_name": "agence", "verbose_name_plural": "agences", "ordering": ["display_order", "country_name"]},
        ),
        migrations.RunPython(seed_agencies, migrations.RunPython.noop),
    ]
