from django.db import migrations


def update_labels(apps, schema_editor):
    TariffPlan = apps.get_model("marketing", "TariffPlan")
    labels = {
        "envoi-vers-tanzanie": ("Tarif spécial Tanzanie", "Transferts envoyés vers ou depuis la Tanzanie"),
        "retrait-hors-tanzanie": ("Tarif retrait quotidien", "Tarif standard du réseau Blue Sky"),
        "envoi-hors-tanzanie": ("Tarif envoi quotidien", "Tarif standard du réseau Blue Sky"),
    }
    for slug, (title, scope_label) in labels.items():
        TariffPlan.objects.filter(slug=slug).update(title=title, scope_label=scope_label)


class Migration(migrations.Migration):
    dependencies = [("marketing", "0003_tariffplan_tariffband")]
    operations = [migrations.RunPython(update_labels, migrations.RunPython.noop)]
