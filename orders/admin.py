from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Affiche les produits directement
    dans la fiche d'une commande.
    """

    model = OrderItem
    extra = 0

    # Ces champs ne doivent pas être modifiés manuellement
    readonly_fields = (
        "product",
        "product_name",
        "unit_price",
        "quantity",
        "display_subtotal",
    )

    fields = (
        "product",
        "product_name",
        "unit_price",
        "quantity",
        "display_subtotal",
    )

    def display_subtotal(self, obj):
        return obj.subtotal

    display_subtotal.short_description = "Sous-total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Colonnes de la liste des commandes
    list_display = (
        "id",
        "customer_name",
        "phone",
        "total",
        "status",
        "created_at",
    )

    # Filtres disponibles dans l'administration
    list_filter = (
        "status",
        "created_at",
    )

    # Recherche d'une commande
    search_fields = (
        "customer_name",
        "email",
        "phone",
        "address",
    )

    # Statut modifiable depuis la liste
    list_editable = ("status",)

    # Produits affichés dans la commande
    inlines = [OrderItemInline]

    # Informations qui ne doivent pas être modifiées
    readonly_fields = (
        "subtotal",
        "delivery_fee",
        "total",
        "created_at",
        "updated_at",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product_name",
        "unit_price",
        "quantity",
    )