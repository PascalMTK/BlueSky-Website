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
