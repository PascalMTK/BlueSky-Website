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
