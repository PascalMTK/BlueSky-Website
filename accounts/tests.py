import re

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import EmailVerification, User


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AccountVerificationTests(TestCase):
    def signup_data(self, **overrides):
        data = {
            "full_name": "Test Client",
            "email": "client@example.com",
            "phone": "+243900000000",
            "country": "Congo (RDC)",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
        }
        data.update(overrides)
        return data

    def test_password_confirmation_must_match(self):
        response = self.client.post(reverse("accounts:signup"), self.signup_data(password_confirm="Different123!"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Les mots de passe ne correspondent pas")
        self.assertFalse(User.objects.exists())

    def test_signup_creates_inactive_user_and_sends_otp(self):
        response = self.client.post(reverse("accounts:signup"), self.signup_data())
        self.assertRedirects(response, reverse("accounts:verify_otp"))
        user = User.objects.get(email="client@example.com")
        self.assertFalse(user.is_active)
        self.assertTrue(EmailVerification.objects.filter(user=user).exists())
        self.assertEqual(len(mail.outbox), 1)

    def test_valid_otp_activates_and_logs_in_user(self):
        self.client.post(reverse("accounts:signup"), self.signup_data())
        code = re.search(r"\b\d{6}\b", mail.outbox[0].body).group(0)
        response = self.client.post(reverse("accounts:verify_otp"), {"code": code})
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="client@example.com")
        self.assertTrue(user.is_active)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)
        self.assertFalse(EmailVerification.objects.filter(user=user).exists())


class SpaceRoutingTests(TestCase):
    """Each account type lands in, and is limited to, its own space."""

    def setUp(self):
        self.client_user = User.objects.create_user("c@example.com", "Client", "SecurePass123!")
        self.staff_user = User.objects.create_user("s@example.com", "Staff", "SecurePass123!", is_staff=True)

    def login(self, email):
        return self.client.post(reverse("accounts:login"), {"email": email, "password": "SecurePass123!"})

    def test_client_lands_in_client_space(self):
        self.assertRedirects(self.login("c@example.com"), reverse("transfers:overview"), fetch_redirect_response=False)

    def test_staff_lands_in_management_space(self):
        self.assertRedirects(self.login("s@example.com"), reverse("staffpanel:home"), fetch_redirect_response=False)

    def test_client_is_sent_back_from_management_space(self):
        self.client.force_login(self.client_user)
        response = self.client.get(reverse("staffpanel:home"))
        self.assertRedirects(response, reverse("transfers:overview"), fetch_redirect_response=False)

    def test_anonymous_visitor_is_asked_to_sign_in(self):
        response = self.client.get(reverse("staffpanel:home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])

    def test_signed_in_staff_visiting_login_goes_to_management_space(self):
        self.client.force_login(self.staff_user)
        self.assertRedirects(self.client.get(reverse("accounts:login")), reverse("staffpanel:home"), fetch_redirect_response=False)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class BrandedEmailTests(TestCase):
    """Users receive designed e-mails at each important step."""

    def setUp(self):
        from django.core.cache import cache
        cache.clear()

    def signup(self):
        return self.client.post(reverse("accounts:signup"), {
            "full_name": "Marie Kalenga", "email": "marie@example.com", "phone": "+243900000000",
            "country": "Congo (RDC)", "password": "SecurePass123!", "password_confirm": "SecurePass123!",
        })

    def test_otp_email_is_html_with_code_and_reply_to_contact(self):
        from core.data import SITE
        self.signup()
        msg = mail.outbox[0]
        code = re.search(r"\b\d{6}\b", msg.subject).group(0)
        self.assertIn(code, msg.body)
        html = msg.alternatives[0][0]
        self.assertIn(code, html)
        self.assertIn("Votre code de vérification", html)
        self.assertEqual(msg.reply_to, [SITE["primary_email"]])

    def test_welcome_email_after_verification(self):
        self.signup()
        code = re.search(r"\b\d{6}\b", mail.outbox[0].subject).group(0)
        self.client.post(reverse("accounts:verify_otp"), {"code": code})
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn("Bienvenue", mail.outbox[1].subject)

    def test_signup_shows_error_when_code_cannot_be_sent(self):
        from unittest import mock
        with mock.patch("accounts.views.send_verification_code", side_effect=OSError("smtp down")):
            response = self.signup()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pas pu envoyer le code")
        self.assertFalse(User.objects.filter(email="marie@example.com").exists())

    def test_contact_form_sends_acknowledgement(self):
        self.client.post(reverse("marketing:contact"), {
            "full_name": "Grace Mbuyi", "email": "grace@example.com", "country": "", "service": "transfert",
            "message": "Bonjour, quels sont vos horaires ?"})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["grace@example.com"])
        self.assertIn("bien reçu votre message", mail.outbox[0].subject)

    def test_staff_activation_notifies_client(self):
        from savings.models import SavingsAccount
        client = User.objects.create_user(email="c@example.com", full_name="Client Test", password="x12345678")
        staff = User.objects.create_user(email="s@example.com", full_name="Agent Test", password="x12345678", is_staff=True)
        account = SavingsAccount.objects.create(user=client, id_number="AB123", address="Lubumbashi")
        self.client.force_login(staff)
        self.client.post(reverse("staffpanel:activate_account", args=[account.pk]))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["c@example.com"])
        self.assertIn("actif", mail.outbox[0].subject)
