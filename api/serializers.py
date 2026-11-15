from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from orders.models import Order, OrderItem
from restaurant.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Transforme une catégorie Django en données JSON.

    Il permet également de valider les données reçues
    lorsqu'un manager crée ou modifie une catégorie.
    """

    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "is_active",
            "display_order",
        ]

        # L'identifiant est créé automatiquement par Django.
        read_only_fields = [
            "id",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Transforme un produit Django en données JSON.
    """

    # Affiche le nom de la catégorie en plus de son identifiant.
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Product

        fields = [
            "id",
            "category",
            "category_name",
            "name",
            "description",
            "price",
            "image",
            "stock",
            "is_available",
            "created_at",
        ]

        # Ces champs sont renseignés automatiquement.
        read_only_fields = [
            "id",
            "created_at",
        ]


class OrderItemInputSerializer(serializers.Serializer):
    """
    Structure attendue lorsqu'un client commande un produit.

    Le client envoie uniquement :
    - l'identifiant du produit ;
    - la quantité souhaitée.

    Il ne peut pas envoyer le prix ou le nom du produit.
    """

    product_id = serializers.IntegerField(
        min_value=1,
    )

    quantity = serializers.IntegerField(
        min_value=1,
        max_value=100,
    )


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour afficher les produits
    enregistrés dans une commande existante.
    """

    # La propriété subtotal est calculée dans le modèle.
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product",
            "product_name",
            "unit_price",
            "quantity",
            "subtotal",
        ]

        # Les lignes sont entièrement créées par le serveur.
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer principal utilisé pour créer et afficher
    une commande.
    """

    # Affiche les lignes de la commande lors d'un GET.
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    # Champ utilisé uniquement lors de la création.
    # Il ne sera pas affiché dans la réponse finale.
    order_items = OrderItemInputSerializer(
        many=True,
        write_only=True,
    )

    # Affiche le nom d'utilisateur du client connecté.
    customer_username = serializers.CharField(
        source="customer.username",
        read_only=True,
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "customer",
            "customer_username",
            "customer_name",
            "email",
            "phone",
            "address",
            "city",
            "postal_code",
            "delivery_instructions",
            "subtotal",
            "delivery_fee",
            "total",
            "status",
            "created_at",
            "updated_at",
            "items",
            "order_items",
        ]

        # Le client ne doit pas pouvoir modifier ces champs.
        # Ils sont déterminés par le serveur.
        read_only_fields = [
            "id",
            "customer",
            "subtotal",
            "delivery_fee",
            "total",
            "status",
            "created_at",
            "updated_at",
            "items",
        ]

    def validate_order_items(self, value):
        """
        Vérifie que la commande contient au moins un produit
        et qu'un même produit n'est pas envoyé plusieurs fois.
        """

        if not value:
            raise serializers.ValidationError(
                "La commande doit contenir au moins un produit."
            )

        product_ids = [
            item["product_id"]
            for item in value
        ]

        # Refuse les identifiants présents plusieurs fois.
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                "Un produit ne peut apparaître qu'une seule fois."
            )

        return value

    def validate_phone(self, value):
        """
        Nettoie le numéro et vérifie sa longueur minimale.
        """

        cleaned_value = value.strip()

        if len(cleaned_value) < 8:
            raise serializers.ValidationError(
                "Le numéro de téléphone est trop court."
            )

        return cleaned_value

    def validate_postal_code(self, value):
        """
        Vérifie que le code postal contient cinq chiffres.
        Cette règle correspond à une adresse française.
        """

        cleaned_value = value.strip()

        if (
            len(cleaned_value) != 5
            or not cleaned_value.isdigit()
        ):
            raise serializers.ValidationError(
                "Le code postal doit contenir cinq chiffres."
            )

        return cleaned_value

    @transaction.atomic
    def create(self, validated_data):
        """
        Crée la commande et ses lignes dans une transaction.

        Si une opération échoue, Django annule l'ensemble
        de la création afin d'éviter une commande incomplète.
        """

        # Retire les produits des données principales.
        items_data = validated_data.pop(
            "order_items"
        )

        # Récupère la requête HTTP transmise au serializer.
        request = self.context.get("request")

        if request is None:
            raise serializers.ValidationError(
                "La requête est absente."
            )

        # L'API des commandes nécessite un utilisateur connecté.
        if not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Vous devez être connecté pour commander."
            )

        # Liste des identifiants demandés par le client.
        product_ids = [
            item["product_id"]
            for item in items_data
        ]

        # Verrouille les produits pendant la création.
        # Cela limite les problèmes lorsque plusieurs clients
        # commandent simultanément le même produit.
        products = Product.objects.select_for_update().filter(
            id__in=product_ids,
            is_available=True,
            category__is_active=True,
        )

        # Crée un dictionnaire pour retrouver rapidement
        # chaque produit à partir de son identifiant.
        products_by_id = {
            product.id: product
            for product in products
        }

        # Vérifie que tous les produits demandés existent
        # et sont disponibles.
        missing_product_ids = [
            product_id
            for product_id in product_ids
            if product_id not in products_by_id
        ]

        if missing_product_ids:
            raise serializers.ValidationError(
                {
                    "order_items": (
                        "Un ou plusieurs produits sont "
                        "introuvables ou indisponibles."
                    )
                }
            )

        subtotal = Decimal("0.00")

        # Vérifie le stock et calcule le sous-total.
        for item_data in items_data:
            product = products_by_id[
                item_data["product_id"]
            ]

            quantity = item_data["quantity"]

            if quantity > product.stock:
                raise serializers.ValidationError(
                    {
                        "order_items": (
                            f"Stock insuffisant pour "
                            f"{product.name}. "
                            f"Stock disponible : {product.stock}."
                        )
                    }
                )

            subtotal += product.price * quantity

        # Frais actuellement fixes.
        delivery_fee = Decimal("2.50")

        # Le serveur calcule lui-même le total.
        total = subtotal + delivery_fee

        # Crée la commande et associe automatiquement
        # l'utilisateur identifié par son token.
        order = Order.objects.create(
            customer=request.user,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
            **validated_data,
        )

        # Crée les lignes de commande.
        for item_data in items_data:
            product = products_by_id[
                item_data["product_id"]
            ]

            quantity = item_data["quantity"]

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=product.price,
                quantity=quantity,
            )

            # Diminue le stock après la création de la ligne.
            product.stock -= quantity
            product.save(
                update_fields=["stock"]
            )

        return order

class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Serializer réservé aux employés et managers.

    Il permet uniquement de modifier le statut.
    Les prix, le client, l'adresse et les produits
    ne peuvent pas être modifiés ici.
    """

    class Meta:
        model = Order

        fields = [
            "status",
        ]

    def validate_status(self, value):
        """
        Contrôle les changements de statut autorisés.
        """

        # Lors d'une création sans instance,
        # aucun ancien statut n'est disponible.
        if self.instance is None:
            return value

        current_status = self.instance.status

        # Liste des passages autorisés.
        allowed_transitions = {
            "pending": [
                "confirmed",
                "cancelled",
            ],
            "confirmed": [
                "preparing",
                "cancelled",
            ],
            "preparing": [
                "delivering",
                "cancelled",
            ],
            "delivering": [
                "delivered",
            ],
            "delivered": [],
            "cancelled": [],
        }

        allowed_statuses = allowed_transitions.get(
            current_status,
            [],
        )

        # Autorise l'envoi du statut actuel sans changement.
        if value == current_status:
            return value

        if value not in allowed_statuses:
            raise serializers.ValidationError(
                (
                    f"Le passage du statut "
                    f"« {current_status} » vers "
                    f"« {value} » n'est pas autorisé."
                )
            )

        return value