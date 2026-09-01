from django.db import migrations, models
import django.db.models.deletion


def seed_drc_payment_information(apps, schema_editor):
    PaymentLocation = apps.get_model("marketing", "PaymentLocation")
    PaymentAccount = apps.get_model("marketing", "PaymentAccount")
    location = PaymentLocation.objects.create(
        country="République démocratique du Congo",
        city="Lubumbashi",
        cash_address="Avenue Kapenda, coin Mobutu, en face de l'Hôtel Hypnose",
        slogan="L'argent voyage en toute sécurité",
        display_order=1,
    )
    accounts = [
        ("Airtel Money", "+243 989 443 485", "Lord Kasisu", ""),
        ("Airtel Money", "+243 989 555 229", "Kasisu Josephine", ""),
        ("Airtel Money", "+243 989 474 804", "Lord Kasisu", ""),
        ("Airtel Money", "+243 997 266 023", "Elie Kayembe", "Effectuez uniquement un retrait. Aucun dépôt n'est autorisé."),
        ("M-Pesa", "+243 810 005 702", "Josephine Kasisu", ""),
        ("Orange Money", "+243 857 805 518", "Kayembe Elie", ""),
    ]
    PaymentAccount.objects.bulk_create([
        PaymentAccount(location=location, payment_method=method, phone_number=phone, account_holder=holder, instruction=instruction, display_order=index)
        for index, (method, phone, holder, instruction) in enumerate(accounts, start=1)
    ])


class Migration(migrations.Migration):
    dependencies = [("marketing", "0004_rename_public_tariff_labels")]
    operations = [
        migrations.CreateModel(
            name="PaymentLocation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("country", models.CharField(max_length=100, verbose_name="Pays")),
                ("city", models.CharField(blank=True, max_length=100, verbose_name="Ville")),
                ("cash_address", models.TextField(blank=True, verbose_name="Adresse de retrait cash")),
                ("slogan", models.CharField(blank=True, max_length=220, verbose_name="Slogan")),
                ("is_active", models.BooleanField(default=True, verbose_name="Visible pour les clients")),
                ("display_order", models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Dernière modification")),
            ],
            options={"verbose_name": "information de paiement", "verbose_name_plural": "informations de paiement", "ordering": ["display_order", "country", "city"]},
        ),
        migrations.CreateModel(
            name="PaymentAccount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("payment_method", models.CharField(max_length=80, verbose_name="Moyen de paiement")),
                ("phone_number", models.CharField(max_length=40, verbose_name="Numéro")),
                ("account_holder", models.CharField(max_length=140, verbose_name="Titulaire")),
                ("instruction", models.CharField(blank=True, max_length=220, verbose_name="Instruction particulière")),
                ("is_active", models.BooleanField(default=True, verbose_name="Visible")),
                ("display_order", models.PositiveSmallIntegerField(default=0, verbose_name="Ordre")),
                ("location", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="accounts", to="marketing.paymentlocation", verbose_name="Pays / agence")),
            ],
            options={"verbose_name": "compte de paiement", "verbose_name_plural": "comptes de paiement", "ordering": ["display_order", "payment_method", "id"]},
        ),
        migrations.RunPython(seed_drc_payment_information, migrations.RunPython.noop),
    ]
