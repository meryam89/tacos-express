
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from restaurant.models import Category, Product

from .models import Order


class CartAndOrderTests(TestCase):
    """
    Vérifie le panier, les commandes,
    le minimum d'achat et la sécurité.
    """

    def setUp(self):
        """
        Prépare les données nécessaires avant chaque test.

        Django utilise une base de données de test séparée.
        Les vrais produits et leurs prix ne sont pas modifiés.
        """

        # Création d'un utilisateur pour les tests
        self.user = User.objects.create_user(
            username="client",
            password="MotDePasse2026!",
        )

        # Création d'une catégorie
        category = Category.objects.create(
            name="Tacos",
        )

        # Création d'un produit fictif à 7 €
        self.product = Product.objects.create(
            category=category,
            name="Frenchy",
            price=Decimal("7.00"),
            stock=5,
        )

    def get_checkout_data(self):
        """
        Retourne les informations du formulaire de commande.

        Cela évite de répéter le même formulaire
        dans tous les tests.
        """

        return {
            "customer_name": "Client Test",
            "email": "client@example.com",
            "phone": "0600000000",
            "address": "1 rue du Test",
            "city": "Evry",
            "postal_code": "91000",
            "delivery_instructions": "",
        }

    def set_cart_quantity(self, quantity):
        """
        Ajoute le produit fictif au panier
        avec la quantité demandée.
        """

        # Récupération de la session du client
        session = self.client.session

        # Enregistrement du produit et de sa quantité
        session["cart"] = {
            str(self.product.id): quantity,
        }

        # Sauvegarde du panier
        session.save()

    def test_add_product_to_cart(self):
        """
        Vérifie qu'un produit peut être ajouté au panier.
        """

        # Simulation du clic sur "Ajouter au panier"
        response = self.client.post(
            reverse(
                "orders:add_to_cart",
                args=[self.product.id],
            )
        )

        # Vérifie la redirection vers le panier
        self.assertRedirects(
            response,
            reverse("orders:cart"),
        )

        # Vérifie que le panier contient un produit
        self.assertEqual(
            self.client.session["cart"][str(self.product.id)],
            1,
        )

    def test_checkout_creates_order_and_decreases_stock(self):
        """
        Vérifie qu'une commande de 14 € est acceptée
        et que le stock diminue.
        """

        # Connexion du client
        self.client.force_login(self.user)

        # Deux produits à 7 € = 14 €
        self.set_cart_quantity(2)

        # Validation de la commande
        response = self.client.post(
            reverse("orders:checkout"),
            self.get_checkout_data(),
        )

        # Vérifie que la page répond correctement
        self.assertEqual(response.status_code, 200)

        # Vérifie que la commande a été créée
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.get()

        # Vérifie que la commande appartient au client
        self.assertEqual(order.customer, self.user)

        # 14 € de produits + 2,50 € de livraison
        self.assertEqual(
            order.subtotal,
            Decimal("14.00"),
        )
        self.assertEqual(
            order.total,
            Decimal("16.50"),
        )

        # Vérifie le nombre de lignes de commande
        self.assertEqual(order.items.count(), 1)

        # Vérifie que le stock passe de 5 à 3
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        # Vérifie que le panier est vidé
        self.assertEqual(
            self.client.session["cart"],
            {},
        )

    def test_user_cannot_read_another_users_order(self):
        """
        Vérifie qu'un client ne peut pas consulter
        la commande d'un autre utilisateur.
        """

        # Création d'un deuxième utilisateur
        other_user = User.objects.create_user(
            username="autre",
            password="AutreMotDePasse2026!",
        )

        # Création d'une commande appartenant à cet utilisateur
        order = Order.objects.create(
            customer=other_user,
            customer_name="Autre client",
            email="autre@example.com",
            phone="0611111111",
            address="2 rue du Test",
            city="Paris",
            postal_code="75000",
        )

        # Connexion avec le premier utilisateur
        self.client.force_login(self.user)

        # Tentative d'accès à la commande de l'autre client
        response = self.client.get(
            reverse(
                "orders:order_detail",
                args=[order.id],
            )
        )

        # L'accès doit être refusé : erreur 404
        self.assertEqual(response.status_code, 404)

    def test_checkout_refuses_order_below_10_euros(self):
        """
        Vérifie qu'une commande de 7 € est refusée.

        Les frais de livraison ne comptent pas
        dans le minimum de commande.
        """

        # Un produit à 7 € dans le panier
        self.set_cart_quantity(1)

        # Tentative de validation
        response = self.client.post(
            reverse("orders:checkout"),
            self.get_checkout_data(),
        )

        # La page doit rester accessible
        self.assertEqual(response.status_code, 200)

        # Le message d'erreur doit apparaître
        self.assertContains(
            response,
            "Le montant minimum de commande est de 10 €",
        )

        # Aucune commande ne doit être créée
        self.assertEqual(Order.objects.count(), 0)

        # Le stock doit rester à 5
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

        # Le produit doit rester dans le panier
        self.assertEqual(
            self.client.session["cart"][str(self.product.id)],
            1,
        )

    def test_checkout_refuses_order_of_9_99_euros(self):
        """
        Vérifie qu'une commande de 9,99 € est refusée.

        Ce test permet de vérifier que le minimum
        est bien de 10 € exactement.
        """

        # Prix fictif utilisé uniquement pendant ce test
        self.product.price = Decimal("9.99")
        self.product.save()

        # Un produit à 9,99 € dans le panier
        self.set_cart_quantity(1)

        # Tentative de validation
        response = self.client.post(
            reverse("orders:checkout"),
            self.get_checkout_data(),
        )

        # Le message d'erreur doit apparaître
        self.assertContains(
            response,
            "Le montant minimum de commande est de 10 €",
        )

        # Aucune commande ne doit être enregistrée
        self.assertEqual(Order.objects.count(), 0)

        # Le stock ne doit pas changer
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

    def test_checkout_accepts_order_of_exactly_10_euros(self):
        """
        Vérifie qu'une commande de 10 € exactement
        est acceptée.

        Le prix est modifié uniquement dans la base
        de données temporaire des tests.
        """

        # Prix fictif de 10 € pour vérifier la limite
        self.product.price = Decimal("10.00")
        self.product.save()

        # Un produit à 10 € dans le panier
        self.set_cart_quantity(1)

        # Validation de la commande
        response = self.client.post(
            reverse("orders:checkout"),
            self.get_checkout_data(),
        )

        # Vérifie que la page répond correctement
        self.assertEqual(response.status_code, 200)

        # Une commande doit être créée
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.get()

        # Vérifie le sous-total de 10 €
        self.assertEqual(
            order.subtotal,
            Decimal("10.00"),
        )

        # Vérifie les frais de livraison
        self.assertEqual(
            order.delivery_fee,
            Decimal("2.50"),
        )

        # Vérifie le total de 12,50 €
        self.assertEqual(
            order.total,
            Decimal("12.50"),
        )

        # Vérifie que le stock passe de 5 à 4
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 4)

        # Vérifie que le panier est vidé
        self.assertEqual(
            self.client.session["cart"],
            {},
        )
