from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Recipient, Transfer


class PersonalTransferRecordTests(TestCase):
    """Transfers are made at an agency; the client space only records them."""

    def setUp(self):
        self.user = User.objects.create_user(email="client@example.com", full_name="Grace Mbuyi", password="pass12345")
        self.other = User.objects.create_user(email="other@example.com", full_name="Autre Client", password="pass12345")
        self.recipient = Recipient.objects.create(user=self.user, full_name="Jean Kabila", country="Zambie")
        self.client.force_login(self.user)

    def _record(self, **extra):
        data = {"recipient": self.recipient.pk, "amount_sent": "150", "currency_sent": "USD", "payment_method": "M-Pesa", "note": ""}
        data.update(extra)
        return self.client.post(reverse("transfers:new_transfer"), data)

    def test_recorded_transfer_is_saved_as_done_not_queued_for_staff(self):
        response = self._record()
        self.assertRedirects(response, reverse("transfers:overview"))
        transfer = Transfer.objects.get(user=self.user)
        self.assertEqual(transfer.status, Transfer.Status.COMPLETED)
        self.assertEqual(transfer.destination_country, "Zambie")
        self.assertFalse(Transfer.objects.filter(status=Transfer.Status.PENDING).exists())

    def test_client_can_delete_own_record(self):
        self._record()
        transfer = Transfer.objects.get(user=self.user)
        self.client.post(reverse("transfers:delete_transfer", args=[transfer.pk]))
        self.assertFalse(Transfer.objects.filter(pk=transfer.pk).exists())

    def test_client_cannot_delete_someone_elses_record(self):
        theirs = Transfer.objects.create(
            user=self.other, origin_country="RDC", destination_country="Kenya",
            amount_sent=Decimal("50"), currency_sent="USD", payment_method="M-Pesa",
            status=Transfer.Status.COMPLETED,
        )
        self.client.post(reverse("transfers:delete_transfer", args=[theirs.pk]))
        self.assertTrue(Transfer.objects.filter(pk=theirs.pk).exists())

    def test_transfer_being_handled_cannot_be_deleted(self):
        pending = Transfer.objects.create(
            user=self.user, recipient=self.recipient, origin_country="RDC", destination_country="Zambie",
            amount_sent=Decimal("80"), currency_sent="USD", payment_method="M-Pesa",
        )
        self.client.post(reverse("transfers:delete_transfer", args=[pending.pk]))
        self.assertTrue(Transfer.objects.filter(pk=pending.pk).exists())

    def test_overview_counts_records_and_ignores_cancelled(self):
        self._record()
        self._record(amount_sent="50")
        Transfer.objects.create(
            user=self.user, recipient=self.recipient, origin_country="RDC", destination_country="Zambie",
            amount_sent=Decimal("999"), currency_sent="USD", payment_method="M-Pesa",
            status=Transfer.Status.CANCELLED,
        )
        response = self.client.get(reverse("transfers:overview"))
        stats = {label: value for _icon, label, value, _tone in response.context["stats"]}
        self.assertEqual(stats["Transferts enregistrés"], 2)
        self.assertEqual(response.context["sent_totals"][0]["total"], Decimal("200"))
        self.assertContains(response, "pas encore disponibles")


class HomeFeeCalculatorTests(TestCase):
    def test_home_shows_fee_estimate_with_tariff_data(self):
        response = self.client.get(reverse("marketing:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="fee-plans-data"')
        self.assertNotContains(response, "Démarrer un transfert")
