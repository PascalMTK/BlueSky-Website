from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class AccessRulesTests(TestCase):
    """Who may open which space.

    - Clients: their own space only.
    - Team members (is_staff): the management space (/gestion/), not /admin/.
    - Administrators (superusers): both.
    """

    def setUp(self):
        self.client_user = User.objects.create_user(email="client@example.com", full_name="Client Test", password="pass12345")
        self.staff_user = User.objects.create_user(email="staff@example.com", full_name="Equipe Test", password="pass12345", is_staff=True)
        self.admin_user = User.objects.create_superuser(email="admin@example.com", full_name="Admin Test", password="pass12345")

    def test_anonymous_visitor_is_asked_to_log_in(self):
        self.assertRedirects(self.client.get(reverse("staffpanel:home")), f"{reverse('accounts:login')}?next={reverse('staffpanel:home')}")
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response["Location"])

    def test_client_cannot_open_management_space_or_admin_centre(self):
        self.client.force_login(self.client_user)
        self.assertRedirects(self.client.get(reverse("staffpanel:home")), reverse("transfers:overview"))
        self.assertRedirects(self.client.get(reverse("admin:index")), reverse("transfers:overview"))
        self.assertRedirects(self.client.get(reverse("admin:transfers_transfer_changelist")), reverse("transfers:overview"))

    def test_team_member_gets_management_space_but_not_admin_centre(self):
        self.client.force_login(self.staff_user)
        self.assertEqual(self.client.get(reverse("staffpanel:home")).status_code, 200)
        self.assertRedirects(self.client.get(reverse("admin:index")), reverse("staffpanel:home"))
        self.assertRedirects(self.client.get(reverse("admin:blog_post_add")), reverse("staffpanel:home"))

    def test_team_member_does_not_see_admin_centre_link(self):
        self.client.force_login(self.staff_user)
        self.assertNotContains(self.client.get(reverse("staffpanel:home")), reverse("admin:index"))

    def test_administrator_gets_both(self):
        self.client.force_login(self.admin_user)
        self.assertEqual(self.client.get(reverse("staffpanel:home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin:blog_post_add")).status_code, 200)

    def test_client_cannot_log_in_through_admin_login(self):
        response = self.client.post(reverse("admin:login"), {"username": "client@example.com", "password": "pass12345"})
        self.assertEqual(response.status_code, 200)  # form shown again with an error
        self.assertNotIn("_auth_user_id", self.client.session)


class LaunchChecklistTests(TestCase):
    """Privacy/terms pages, robots.txt, sitemap, social previews, anti-spam."""

    def setUp(self):
        from django.core.cache import cache
        cache.clear()

    def test_legal_pages_exist_and_are_linked_in_footer(self):
        for name in ("marketing:privacy", "marketing:terms"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        home = self.client.get(reverse("marketing:home"))
        self.assertContains(home, reverse("marketing:privacy"))
        self.assertContains(home, reverse("marketing:terms"))

    def test_robots_and_sitemap(self):
        robots = self.client.get("/robots.txt")
        self.assertEqual(robots.status_code, 200)
        self.assertContains(robots, "Disallow: /admin/")
        self.assertContains(robots, "sitemap.xml")
        sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap["Content-Type"], "application/xml; charset=utf-8")
        self.assertContains(sitemap, reverse("marketing:tariffs"))
        self.assertNotContains(sitemap, "/gestion/")

    def test_social_preview_and_cookie_banner(self):
        home = self.client.get(reverse("marketing:home"))
        self.assertContains(home, 'property="og:image"')
        self.assertContains(home, "og-image.jpg")
        self.assertContains(home, "data-cookie-banner")

    def test_contact_honeypot_drops_spam_silently(self):
        from marketing.models import ContactMessage

        data = {"full_name": "Robot", "email": "bot@example.com", "country": "", "service": "transfert",
                "message": "Buy cheap things now please", "website": "http://spam.example"}
        response = self.client.post(reverse("marketing:contact"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["sent"])
        self.assertFalse(ContactMessage.objects.exists())

    def test_contact_rate_limit(self):
        from marketing.models import ContactMessage

        data = {"full_name": "Grace", "email": "grace@example.com", "country": "", "service": "transfert",
                "message": "Bonjour, quels sont vos horaires ?"}
        for _ in range(7):
            self.client.post(reverse("marketing:contact"), data)
        self.assertEqual(ContactMessage.objects.count(), 5)
