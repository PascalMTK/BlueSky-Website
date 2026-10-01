from django.test import TestCase


class SiteBasicsTests(TestCase):
    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Disallow: /gestion/")

    def test_pages_have_link_preview_tags(self):
        response = self.client.get("/")
        self.assertContains(response, 'property="og:image"')
