from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Transfer


class OverviewStatsTests(TestCase):
    def test_stats_count_every_transfer_not_only_the_recent_list(self):
        user = User.objects.create_user("client@example.com", "Test Client", "SecurePass123!")
        for _ in range(10):
            Transfer.objects.create(
                user=user, origin_country="Congo (RDC)", destination_country="Zambie",
                amount_sent=100, currency_sent="USD", payment_method="M-Pesa",
            )
        self.client.force_login(user)

        response = self.client.get(reverse("transfers:overview"))

        self.assertEqual(len(response.context["transfers"]), 8)
        self.assertEqual(response.context["stats"][0][2], 10)
        self.assertEqual(response.context["stats"][1][2], 10)
