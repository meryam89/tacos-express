from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order
from restaurant.models import Category, Product
from .permissions import (
    IsEmployeeOrManager,
    IsManagerOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    OrderSerializer,
    OrderStatusSerializer,
    ProductSerializer,
)
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [
        IsManagerOrReadOnly,
    ]

    def get_queryset(self):
        user = self.request.user

        if (
            user.is_authenticated
            and user.groups.filter(name="Managers").exists()
        ):
            return Category.objects.all()

        return Category.objects.filter(
            is_active=True
        )


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [
        IsManagerOrReadOnly,
    ]

    def get_queryset(self):
        user = self.request.user

        queryset = Product.objects.select_related(
            "category"
        )

        if (
            user.is_authenticated
            and user.groups.filter(name="Managers").exists()
        ):
            return queryset

        return queryset.filter(
            is_available=True,
            stock__gt=0,
            category__is_active=True,
        )



class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    API permettant au client connecté :

    - de créer une commande ;
    - de consulter ses commandes ;
    - de consulter le détail d'une de ses commandes.

    Les actions de modification et de suppression
    ne sont volontairement pas disponibles au client.
    """

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        """
        Retourne uniquement les commandes
        appartenant à l'utilisateur connecté.
        """

        return (
            Order.objects
            .filter(customer=self.request.user)
            .prefetch_related(
                "items",
                "items__product",
            )
        )


class StaffOrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    API réservée aux employés et aux managers.

    Elle permet :
    - de consulter toutes les commandes ;
    - de consulter une commande ;
    - de modifier uniquement son statut.
    """

    serializer_class = OrderSerializer

    permission_classes = [
        IsEmployeeOrManager,
    ]

    def get_queryset(self):
        """
        Retourne toutes les commandes avec leurs clients
        et leurs produits.
        """

        return (
            Order.objects
            .select_related("customer")
            .prefetch_related(
                "items",
                "items__product",
            )
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="status",
    )
    def update_status(self, request, pk=None):
        """
        Modifie uniquement le statut d'une commande.

        Exemple :
        PATCH /api/staff/orders/4/status/
        """

        # Récupère la commande demandée.
        order = self.get_object()

        # Valide uniquement le nouveau statut.
        status_serializer = OrderStatusSerializer(
            order,
            data=request.data,
            partial=True,
        )

        status_serializer.is_valid(
            raise_exception=True
        )

        # Enregistre le nouveau statut.
        status_serializer.save()

        # Retourne ensuite la commande complète.
        order_serializer = OrderSerializer(
            order,
            context=self.get_serializer_context(),
        )

        return Response(
            order_serializer.data
        )