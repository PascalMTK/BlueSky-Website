import re
import smtplib
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import EmailVerification, User
from .views import OTPDeliveryError, _send_otp


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AccountVerificationTests(TestCase):
    def test_failed_resend_preserves_existing_code(self):
        user = User.objects.create_user("retry@example.com", "Test Client", "SecurePass123!", is_active=False)
        verification, code = EmailVerification.issue_for(user)
        original_hash = verification.code_hash
        with patch("accounts.views.send_mail", side_effect=smtplib.SMTPException("SMTP is down")):
            with self.assertRaises(OTPDeliveryError):
                _send_otp(user)
        verification.refresh_from_db()
        self.assertEqual(verification.code_hash, original_hash)
        self.assertTrue(verification.verify(code))

    def test_https_login_rejects_http_redirect(self):
        User.objects.create_user("client@example.com", "Test Client", "SecurePass123!")
        response = self.client.post(
            reverse("accounts:login"),
            {"email": "client@example.com", "password": "SecurePass123!", "next": "http://testserver/private/"},
            secure=True,
        )
        self.assertRedirects(response, reverse("transfers:overview"), fetch_redirect_response=False)

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

    def test_other_country_saves_the_typed_country(self):
        self.client.post(
            reverse("accounts:signup"),
            self.signup_data(country="Autre", other_country="Angola"),
        )
        self.assertEqual(User.objects.get(email="client@example.com").country, "Angola")

    def test_other_country_requires_a_name(self):
        response = self.client.post(reverse("accounts:signup"), self.signup_data(country="Autre"))
        self.assertContains(response, "Entrez le nom de votre pays")
        self.assertFalse(User.objects.exists())

    def test_common_password_is_rejected(self):
        response = self.client.post(
            reverse("accounts:signup"),
            self.signup_data(password="password123", password_confirm="password123"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.exists())

    @override_settings(EMAIL_BACKEND="accounts.tests.FailingEmailBackend")
    def test_email_failure_shows_message_instead_of_crashing(self):
        response = self.client.post(reverse("accounts:signup"), self.signup_data())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pas pu envoyer le code")
        # Rolled back, so the visitor can retry with the same address.
        self.assertFalse(User.objects.exists())

    def test_too_many_wrong_codes_asks_for_a_new_one(self):
        self.client.post(reverse("accounts:signup"), self.signup_data())
        for _ in range(EmailVerification.MAX_ATTEMPTS):
            self.client.post(reverse("accounts:verify_otp"), {"code": "000000"})
        response = self.client.post(reverse("accounts:verify_otp"), {"code": "000000"})
        self.assertContains(response, "Trop de tentatives")


class FailingEmailBackend:
    def __init__(self, *args, **kwargs):
        pass

    def send_messages(self, messages):
        raise smtplib.SMTPException("SMTP is down")
