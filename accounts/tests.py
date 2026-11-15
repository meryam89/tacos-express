from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class AccountTests(TestCase):
    """Vérifie l'inscription et la protection du profil."""

    def test_registration_creates_client_account(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "nouveauclient",
                "first_name": "Nora",
                "last_name": "Test",
                "email": "nora@example.com",
                "password1": "MotDePasseSolide2026!",
                "password2": "MotDePasseSolide2026!",
            },
        )

        self.assertRedirects(response, reverse("accounts:login"))
        user = User.objects.get(username="nouveauclient")
        self.assertTrue(user.check_password("MotDePasseSolide2026!"))
        self.assertTrue(
            user.groups.filter(name="Clients").exists()
        )
        self.assertTrue(Group.objects.filter(name="Clients").exists())

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("accounts:profile"))

        expected_url = (
            f"{reverse('accounts:login')}?next="
            f"{reverse('accounts:profile')}"
        )
        self.assertRedirects(response, expected_url)

# Create your tests here.
