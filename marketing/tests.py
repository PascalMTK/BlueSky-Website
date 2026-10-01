from django.test import TestCase
from django.urls import reverse

from .models import Agency


class AgencyDisplayTests(TestCase):
    def test_admin_managed_contact_details_are_displayed(self):
        Agency.objects.create(
            code="BW", country_name="Botswana", flag="🇧🇼",
            address="Gaborone", phone_numbers="+267 111 222\n+267 333 444",
            display_order=1,
        )

        response = self.client.get(reverse("marketing:countries"))

        self.assertContains(response, "Gaborone")
        self.assertContains(response, "+267 111 222")
        self.assertContains(response, "+267 333 444")
        # No flag photo exists for BW: the card falls back to the emoji
        # instead of rendering a broken image.
        self.assertNotContains(response, "flags/bw.")

    def test_known_countries_use_flag_photos(self):
        # The nine agencies are seeded by migration 0006.
        response = self.client.get(reverse("marketing:countries"))
        self.assertContains(response, "img/flags/zm.jpg")
