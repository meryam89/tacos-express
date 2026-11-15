from django.db.models import Prefetch
from django.shortcuts import render

from .models import Category, Product


def home(request):
    """
    Affiche une page d'accueil compacte
    avec seulement trois produits.
    """

    featured_products = Product.objects.filter(
        is_available=True,
        stock__gt=0,
    ).select_related(
        "category",
    ).order_by(
        "category__display_order",
        "name",
    )[:3]

    return render(
        request,
        "restaurant/home.html",
        {
            "featured_products": featured_products,
        },
    )


def menu(request):
    """
    Récupère les catégories actives avec leurs produits disponibles.
    """

    available_products = Product.objects.filter(
        is_available=True,
        stock__gt=0,
    )

    categories = Category.objects.filter(
        is_active=True,
    ).prefetch_related(
        Prefetch(
            "products",
            queryset=available_products,
        )
    )

    return render(
        request,
        "restaurant/menu.html",
        {
            "categories": categories,
        },
    )
