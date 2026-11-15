from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class RestaurantTests(TestCase):
    """Vérifie l'affichage des produits disponibles."""

    def setUp(self):
        self.category = Category.objects.create(
            name="Tacos",
            display_order=1,
        )
        self.available_product = Product.objects.create(
            category=self.category,
            name="Tacos test",
            price=Decimal("7.00"),
            stock=5,
            is_available=True,
        )
        self.unavailable_product = Product.objects.create(
            category=self.category,
            name="Produit masqué",
            price=Decimal("5.00"),
            stock=0,
            is_available=False,
        )

    def test_menu_displays_only_available_products(self):
        response = self.client.get(reverse("restaurant:menu"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.available_product.name)
        self.assertNotContains(response, self.unavailable_product.name)

    def test_home_page_is_accessible(self):
        response = self.client.get(reverse("restaurant:home"))

        self.assertEqual(response.status_code, 200)

# Create your tests here.
