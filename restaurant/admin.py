from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste des catégories
    list_display = (
        "name",
        "display_order",
        "is_active",
    )

    # Champs modifiables directement depuis la liste
    list_editable = (
        "display_order",
        "is_active",
    )

    # Barre de recherche
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste des produits
    list_display = [
        "name",
        "category",
        "price",
        "stock",
        "display_order",
        "is_available",
    ]
    # Filtres disponibles à droite
    list_filter = (
        "category",
        "is_available",
    )

    # Champs modifiables directement depuis la liste
    list_editable = [
        "price",
        "stock",
        "display_order",
        "is_available",
    ]

    # Recherche par nom ou description
    search_fields = (
        "name",
        "description",
    )