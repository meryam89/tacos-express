from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from restaurant.models import Category, Product

from .models import Order


class CartAndOrderTests(TestCase):
    """Vérifie le panier, la commande et l'accès aux commandes."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="client",
            password="MotDePasse2026!",
        )
        category = Category.objects.create(name="Tacos")
        self.product = Product.objects.create(
            category=category,
            name="Frenchy",
            price=Decimal("7.00"),
            stock=5,
        )

    def test_add_product_to_cart(self):
        response = self.client.post(
            reverse("orders:add_to_cart", args=[self.product.id])
        )

        self.assertRedirects(response, reverse("orders:cart"))
        self.assertEqual(
            self.client.session["cart"][str(self.product.id)],
            1,
        )

    def test_checkout_creates_order_and_decreases_stock(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["cart"] = {str(self.product.id): 2}
        session.save()

        response = self.client.post(
            reverse("orders:checkout"),
            {
                "customer_name": "Client Test",
                "email": "client@example.com",
                "phone": "0600000000",
                "address": "1 rue du Test",
                "city": "Evry",
                "postal_code": "91000",
                "delivery_instructions": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        order = Order.objects.get()
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.total, Decimal("16.50"))
        self.assertEqual(order.items.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        self.assertEqual(self.client.session["cart"], {})

    def test_user_cannot_read_another_users_order(self):
        other_user = User.objects.create_user(
            username="autre",
            password="AutreMotDePasse2026!",
        )
        order = Order.objects.create(
            customer=other_user,
            customer_name="Autre client",
            email="autre@example.com",
            phone="0611111111",
            address="2 rue du Test",
            city="Paris",
            postal_code="75000",
        )
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("orders:order_detail", args=[order.id])
        )

        self.assertEqual(response.status_code, 404)

# Create your tests here.
