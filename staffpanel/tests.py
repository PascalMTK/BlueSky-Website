from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from savings.models import SavingsAccount, SavingsOperation


class StaffAccessTests(TestCase):
    def test_anonymous_user_is_sent_to_login_with_encoded_next(self):
        response = self.client.get(reverse("staffpanel:transfers") + "?status=PENDING")
        self.assertRedirects(
            response,
            reverse("accounts:login") + "?next=%2Fgestion%2Ftransferts%2F%3Fstatus%3DPENDING",
            fetch_redirect_response=False,
        )

    def test_member_gets_branded_403(self):
        member = User.objects.create_user("client@example.com", "Test Client", "SecurePass123!")
        self.client.force_login(member)
        response = self.client.get(reverse("staffpanel:home"))
        self.assertContains(response, "Erreur 403", status_code=403)


class ConfirmOperationTests(TestCase):
    def setUp(self):
        staff = User.objects.create_user(
            "staff@example.com", "Staff Member", "SecurePass123!", is_staff=True
        )
        member = User.objects.create_user("client@example.com", "Test Client", "SecurePass123!")
        self.account = SavingsAccount.objects.create(
            user=member, id_number="123", address="Lubumbashi",
            status=SavingsAccount.Status.ACTIVE, balance=Decimal("100"),
        )
        self.client.force_login(staff)

    def confirm(self, operation_type, amount):
        operation = SavingsOperation.objects.create(
            account=self.account, operation_type=operation_type, amount=Decimal(amount),
        )
        self.client.post(reverse("staffpanel:confirm_operation", args=[operation.pk]))
        operation.refresh_from_db()
        self.account.refresh_from_db()
        return operation

    def test_deposit_updates_balance(self):
        operation = self.confirm(SavingsOperation.Type.DEPOSIT, "25")
        self.assertEqual(operation.status, SavingsOperation.Status.CONFIRMED)
        self.assertEqual(operation.previous_balance, Decimal("100"))
        self.assertEqual(self.account.balance, Decimal("125"))

    def test_withdrawal_above_balance_is_refused(self):
        operation = self.confirm(SavingsOperation.Type.WITHDRAWAL, "500")
        self.assertEqual(operation.status, SavingsOperation.Status.PENDING)
        self.assertEqual(self.account.balance, Decimal("100"))

    def test_confirmed_operation_cannot_be_rejected_or_confirmed_again(self):
        operation = self.confirm(SavingsOperation.Type.DEPOSIT, "25")
        for action in ("reject_operation", "confirm_operation"):
            response = self.client.post(reverse(f"staffpanel:{action}", args=[operation.pk]))
            self.assertEqual(response.status_code, 404)
        operation.refresh_from_db()
        self.account.refresh_from_db()
        self.assertEqual(operation.status, SavingsOperation.Status.CONFIRMED)
        self.assertEqual(self.account.balance, Decimal("125"))
