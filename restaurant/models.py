from django.db import models

# Create your models here.
class Category(models.Model):
    # Nom de la catégorie : Burgers, Tacos, Desserts...
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom",
    )

    # Permet d'afficher ou masquer une catégorie
    is_active = models.BooleanField(
        default=True,
        verbose_name="Catégorie active",
    )

    # Ordre d'affichage dans le menu
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["display_order", "name"]

    def __str__(self):
        # Texte affiché dans l'administration
        return self.name


class Product(models.Model):
    # Catégorie à laquelle appartient le produit
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Catégorie",
    )

    # Nom du produit
    name = models.CharField(
        max_length=150,
        verbose_name="Nom",
    )

    # Description ou composition du produit
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )

    # Prix avec deux chiffres après la virgule
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Prix",
    )

    # Photo enregistrée dans media/products/
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Image",
    )

    # Quantité disponible
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock",
    )

    # Permet d'afficher ou masquer le produit
    is_available = models.BooleanField(
        default=True,
        verbose_name="Produit disponible",
    )
    # Ordre d'affichage dans une catégorie
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    # Date de création automatique
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = [
            "category",
            "display_order",
            "name",
        ]

    def __str__(self):
        return self.name