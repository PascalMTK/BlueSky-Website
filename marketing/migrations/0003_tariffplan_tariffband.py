from decimal import Decimal

from django.db import migrations, models
import django.db.models.deletion


def seed_tariffs(apps, schema_editor):
    TariffPlan = apps.get_model("marketing", "TariffPlan")
    TariffBand = apps.get_model("marketing", "TariffBand")

    plans = [
        {
            "slug": "envoi-vers-tanzanie",
            "title": "Tarif spécial Tanzanie",
            "scope_label": "Transferts envoyés vers ou depuis la Tanzanie",
            "tariff_type": "send",
            "slogan": "Envoyez de l'argent en toute sécurité",
            "display_order": 1,
            "bands": [(2, 5, "fixed", 1), (6, 19, "fixed", 2), (20, 39, "fixed", 3), (40, 59, "fixed", 4), (60, 99, "fixed", 5), (100, 7500, "percentage", 4), (7501, None, "percentage", 3)],
        },
        {
            "slug": "retrait-hors-tanzanie",
            "title": "Tarif retrait quotidien",
            "scope_label": "Tarif standard du réseau Blue Sky",
            "tariff_type": "withdrawal",
            "slogan": "L'argent voyage en toute sécurité",
            "display_order": 2,
            "bands": [(1, 9, "fixed", 1), (10, 19, "fixed", 2), (20, 39, "fixed", 3), (40, 69, "fixed", 4), (70, 99, "fixed", 5), (100, 3000, "percentage", 5), (3001, 6000, "percentage", 4), (6001, None, "percentage", 3)],
        },
        {
            "slug": "envoi-hors-tanzanie",
            "title": "Tarif envoi quotidien",
            "scope_label": "Tarif standard du réseau Blue Sky",
            "tariff_type": "send",
            "slogan": "L'argent voyage en toute sécurité",
            "display_order": 3,
            "bands": [(1, 25, "fixed", 2), (26, 50, "fixed", 4), (51, 99, "fixed", 6), (100, 3000, "percentage", 5), (3001, None, "percentage", 3)],
        },
    ]

    for plan_data in plans:
        bands = plan_data.pop("bands")
        plan = TariffPlan.objects.create(**plan_data)
        TariffBand.objects.bulk_create([
            TariffBand(
                plan=plan,
                min_amount=Decimal(str(minimum)),
                max_amount=Decimal(str(maximum)) if maximum is not None else None,
                fee_type=fee_type,
                fee_value=Decimal(str(fee)),
                display_order=index,
            )
            for index, (minimum, maximum, fee_type, fee) in enumerate(bands, start=1)
        ])


def remove_seed_tariffs(apps, schema_editor):
    apps.get_model("marketing", "TariffPlan").objects.filter(
        slug__in=["envoi-vers-tanzanie", "retrait-hors-tanzanie", "envoi-hors-tanzanie"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("marketing", "0002_contactmessage_service")]

    operations = [
        migrations.CreateModel(
            name="TariffPlan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(unique=True, verbose_name="Identifiant")),
                ("title", models.CharField(max_length=160, verbose_name="Titre")),
                ("scope_label", models.CharField(max_length=220, verbose_name="Pays concernés")),
                ("tariff_type", models.CharField(choices=[("send", "Envoi"), ("withdrawal", "Retrait")], max_length=20, verbose_name="Type")),
                ("slogan", models.CharField(blank=True, max_length=220, verbose_name="Slogan")),
                ("is_active", models.BooleanField(default=True, verbose_name="Visible sur le site")),
                ("display_order", models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Dernière modification")),
            ],
            options={"verbose_name": "grille tarifaire", "verbose_name_plural": "grilles tarifaires", "ordering": ["display_order", "id"]},
        ),
        migrations.CreateModel(
            name="TariffBand",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("min_amount", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Montant minimum ($)")),
                ("max_amount", models.DecimalField(blank=True, decimal_places=2, help_text="Laissez vide pour une tranche sans limite.", max_digits=12, null=True, verbose_name="Montant maximum ($)")),
                ("fee_type", models.CharField(choices=[("fixed", "Montant fixe ($)"), ("percentage", "Pourcentage (%)")], max_length=16, verbose_name="Type de frais")),
                ("fee_value", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Valeur des frais")),
                ("display_order", models.PositiveSmallIntegerField(default=0, verbose_name="Ordre")),
                ("plan", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bands", to="marketing.tariffplan", verbose_name="Grille tarifaire")),
            ],
            options={"verbose_name": "tranche tarifaire", "verbose_name_plural": "tranches tarifaires", "ordering": ["display_order", "min_amount", "id"]},
        ),
        migrations.RunPython(seed_tariffs, remove_seed_tariffs),
    ]
