from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import SavingsAccount, SavingsOperation


class SavingsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("client@example.com", "Test Client", "SecurePass123!")
        self.account = SavingsAccount.objects.create(
            user=self.user, id_number="123", address="Lubumbashi",
            status=SavingsAccount.Status.ACTIVE, balance=Decimal("50"),
        )
        SavingsOperation.objects.create(
            account=self.account, operation_type=SavingsOperation.Type.DEPOSIT,
            amount=Decimal("50"), status=SavingsOperation.Status.CONFIRMED,
        )
        self.client.force_login(self.user)

    def test_invalid_request_keeps_totals_visible(self):
        response = self.client.post(
            reverse("savings:request_operation"),
            {"operation_type": "WITHDRAWAL", "amount": "500"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["totals"]["deposits"], Decimal("50"))
        self.assertContains(response, "Solde insuffisant")

    def test_valid_request_is_created_and_confirmed_to_the_user(self):
        response = self.client.post(
            reverse("savings:request_operation"),
            {"operation_type": "DEPOSIT", "amount": "20"},
            follow=True,
        )
        self.assertContains(response, "Votre demande a été envoyée")
        self.assertTrue(
            self.account.operations.filter(status=SavingsOperation.Status.PENDING).exists()
        )
