from django.conf import settings
from django.db import models

from restaurant.models import Product


class Order(models.Model):
    """
    Commande effectuée par un client.
    """

    # Différents états possibles de la commande
    STATUS_CHOICES = [
        ("pending", "Commande reçue"),
        ("confirmed", "Commande confirmée"),
        ("preparing", "En préparation"),
        ("delivering", "En livraison"),
        ("delivered", "Commande livrée"),
        ("cancelled", "Commande annulée"),
    ]

    # Compte utilisateur associé à la commande.
    # Il est facultatif afin d'autoriser une commande sans compte.
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="orders",
        blank=True,
        null=True,
        verbose_name="Client",
    )

    # Coordonnées du client
    customer_name = models.CharField(
        max_length=150,
        verbose_name="Nom complet",
    )

    email = models.EmailField(
        verbose_name="Adresse e-mail",
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
    )

    # Adresse de livraison
    address = models.CharField(
        max_length=255,
        verbose_name="Adresse de livraison",
    )

    city = models.CharField(
        max_length=100,
        verbose_name="Ville",
    )

    postal_code = models.CharField(
        max_length=10,
        verbose_name="Code postal",
    )

    # Informations supplémentaires facultatives
    delivery_instructions = models.TextField(
        blank=True,
        verbose_name="Instructions de livraison",
    )

    # Montants enregistrés au moment de la commande
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Sous-total",
    )

    delivery_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=2.50,
        verbose_name="Frais de livraison",
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total",
    )

    # État actuel de la commande
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Statut",
    )

    # Dates créées automatiquement par Django
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification",
    )

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commande #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    """
    Produit enregistré dans une commande.
    """

    # Commande contenant ce produit
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Commande",
    )

    # Produit d'origine.
    # SET_NULL conserve la commande si le produit est supprimé.
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Produit",
    )

    # Copie du nom et du prix au moment de la commande
    product_name = models.CharField(
        max_length=150,
        verbose_name="Nom du produit",
    )

    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Prix unitaire",
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantité",
    )

    class Meta:
        verbose_name = "Produit commandé"
        verbose_name_plural = "Produits commandés"

    @property
    def subtotal(self):
        # Calcule le montant de cette ligne
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product_name}"