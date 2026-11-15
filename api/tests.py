from decimal import Decimal

from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Order
from restaurant.models import Category, Product


class ApiSecurityTests(APITestCase):
    """Vérifie JWT, les rôles et l'isolation des commandes."""

    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client_api",
            password="MotDePasse2026!",
        )
        self.other_user = User.objects.create_user(
            username="autre_client",
            password="MotDePasse2026!",
        )
        self.manager = User.objects.create_user(
            username="manager",
            password="MotDePasse2026!",
        )
        manager_group = Group.objects.create(name="Managers")
        self.manager.groups.add(manager_group)

        self.category = Category.objects.create(
            name="Tacos API",
            display_order=1,
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Produit API",
            price=Decimal("7.00"),
            stock=10,
        )
        self.own_order = Order.objects.create(
            customer=self.client_user,
            customer_name="Client API",
            email="client@example.com",
            phone="0600000000",
            address="1 rue API",
            city="Evry",
            postal_code="91000",
            subtotal=Decimal("7.00"),
            total=Decimal("9.50"),
        )
        Order.objects.create(
            customer=self.other_user,
            customer_name="Autre client",
            email="autre@example.com",
            phone="0611111111",
            address="2 rue API",
            city="Paris",
            postal_code="75000",
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_orders_require_authentication(self):
        response = self.client.get("/api/orders/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_credentials_return_jwt_tokens(self):
        response = self.client.post(
            "/api/auth/token/",
            {
                "username": "client_api",
                "password": "MotDePasse2026!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_client_sees_only_own_orders(self):
        self.authenticate(self.client_user)

        response = self.client.get("/api/orders/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.own_order.id)

    def test_client_cannot_create_product(self):
        self.authenticate(self.client_user)

        response = self.client.post(
            "/api/products/",
            {
                "category": self.category.id,
                "name": "Produit interdit",
                "price": "5.00",
                "stock": 1,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_create_product(self):
        self.authenticate(self.manager)

        response = self.client.post(
            "/api/products/",
            {
                "category": self.category.id,
                "name": "Produit manager",
                "description": "Créé pendant le test",
                "price": "5.00",
                "stock": 1,
                "is_available": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_cannot_skip_order_status(self):
        self.authenticate(self.manager)

        response = self.client.patch(
            f"/api/staff/orders/{self.own_order.id}/status/",
            {"status": "delivered"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Les tests de l'API seront ajoutés ici.
