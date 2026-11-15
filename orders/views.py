from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from restaurant.models import Product

from .forms import CheckoutForm
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required


def get_cart_details(request):
    """
    Transforme le panier enregistré dans la session
    en une liste contenant les produits et les prix.
    """

    # Récupère le panier de la session.
    # Si le panier n'existe pas, Django retourne un dictionnaire vide.
    cart = request.session.get("cart", {})

    # Récupère les produits correspondant aux identifiants du panier
    products = Product.objects.filter(
        id__in=cart.keys(),
        is_available=True,
    )

    items = []
    total = Decimal("0.00")

    for product in products:
        product_key = str(product.id)

        # Quantité enregistrée dans la session
        quantity = int(cart.get(product_key, 0))

        # Prix du produit multiplié par la quantité
        subtotal = product.price * quantity

        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

        total += subtotal

    return items, total


def cart_detail(request):
    """
    Affiche le contenu du panier.
    """

    items, total = get_cart_details(request)

    return render(
        request,
        "orders/cart.html",
        {
            "items": items,
            "total": total,
        },
    )


@require_POST
def add_to_cart(request, product_id):
    """
    Ajoute un produit au panier.
    Cette vue accepte uniquement les requêtes POST.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True,
    )

    # Récupère le panier actuel
    cart = request.session.get("cart", {})

    # Les clés des sessions sont enregistrées sous forme de texte
    product_key = str(product.id)

    # Quantité déjà présente dans le panier
    current_quantity = int(
        cart.get(product_key, 0)
    )

    # Vérifie que le stock permet l'ajout
    if current_quantity < product.stock:
        cart[product_key] = current_quantity + 1

    # Enregistre le panier dans la session
    request.session["cart"] = cart
    request.session.modified = True

    return redirect("orders:cart")
@require_POST
def update_cart(request, product_id):
    """
    Augmente ou diminue la quantité d'un produit.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True,
    )

    cart = request.session.get("cart", {})
    product_key = str(product.id)

    # Si le produit n'est pas dans le panier,
    # on retourne directement à la page du panier.
    if product_key not in cart:
        return redirect("orders:cart")

    quantity = int(cart[product_key])
    action = request.POST.get("action")

    # Augmente la quantité sans dépasser le stock
    if action == "increase":
        if quantity < product.stock:
            cart[product_key] = quantity + 1

    # Diminue la quantité
    elif action == "decrease":
        if quantity > 1:
            cart[product_key] = quantity - 1
        else:
            # Si la quantité atteint zéro,
            # le produit est supprimé.
            del cart[product_key]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("orders:cart")


@require_POST
def remove_from_cart(request, product_id):
    """
    Supprime complètement un produit du panier.
    """

    cart = request.session.get("cart", {})
    product_key = str(product_id)

    if product_key in cart:
        del cart[product_key]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("orders:cart")

def checkout(request):
    """
    Affiche le formulaire puis enregistre
    la commande et ses produits.
    """

    items, subtotal = get_cart_details(request)

    # Empêche de commander avec un panier vide
    if not items:
        return redirect("restaurant:menu")

    # Frais fixes de livraison
    delivery_fee = Decimal("2.50")
    total = subtotal + delivery_fee

    # POST si le client valide le formulaire,
    # sinon formulaire vide.
    form = CheckoutForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        order = None
        stock_error = False
        locked_items = []

        # La transaction garantit que toutes les opérations
        # sont enregistrées ensemble.
        with transaction.atomic():
            for item in items:
                product = Product.objects.select_for_update().get(
                    id=item["product"].id
                )

                quantity = item["quantity"]

                # Nouvelle vérification du stock
                if quantity > product.stock:
                    form.add_error(
                        None,
                        (
                            f"Le stock de {product.name} "
                            "est insuffisant."
                        ),
                    )
                    stock_error = True
                    break

                locked_items.append(
                    {
                        "product": product,
                        "quantity": quantity,
                    }
                )

            if not stock_error:
                # Création de la commande sans l'enregistrer immédiatement
                order = form.save(commit=False)

                # Associe la commande au compte si le client est connecté
                if request.user.is_authenticated:
                    order.customer = request.user

                order.subtotal = subtotal
                order.delivery_fee = delivery_fee
                order.total = total
                order.save()

                # Enregistre chaque produit de la commande
                for item in locked_items:
                    product = item["product"]
                    quantity = item["quantity"]

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        unit_price=product.price,
                        quantity=quantity,
                    )

                    # Retire la quantité commandée du stock
                    product.stock -= quantity

                    if product.stock == 0:
                        product.is_available = False

                    product.save(
                        update_fields=[
                            "stock",
                            "is_available",
                        ]
                    )

        if order is not None:
            # Vide le panier après la commande
            request.session["cart"] = {}
            request.session.modified = True

            return render(
                request,
                "orders/order_success.html",
                {
                    "order": order,
                },
            )

    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "items": items,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "total": total,
        },
    )

@login_required
def order_history(request):
    """
    Affiche uniquement les commandes
    appartenant à l'utilisateur connecté.
    """

    orders = Order.objects.filter(
        customer=request.user,
    ).prefetch_related(
        "items",
    )

    return render(
        request,
        "orders/order_history.html",
        {
            "orders": orders,
        },
    )

@login_required
def order_detail(request, order_id):
    """
    Affiche le détail d'une commande appartenant
    uniquement à l'utilisateur connecté.
    """

    order = get_object_or_404(
        Order.objects.prefetch_related("items"),
        id=order_id,
        customer=request.user,
    )

    # Étapes normales d'une livraison
    delivery_steps = [
        ("pending", "Commande reçue"),
        ("confirmed", "Commande confirmée"),
        ("preparing", "En préparation"),
        ("delivering", "En livraison"),
        ("delivered", "Commande livrée"),
    ]

    status_values = [
        status
        for status, label in delivery_steps
    ]

    try:
        current_position = status_values.index(
            order.status
        )
    except ValueError:
        # Par exemple, une commande annulée
        current_position = -1

    steps = []

    for position, (status, label) in enumerate(
        delivery_steps
    ):
        steps.append(
            {
                "status": status,
                "label": label,
                "completed": position <= current_position,
                "current": position == current_position,
            }
        )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
            "steps": steps,
        },
    )