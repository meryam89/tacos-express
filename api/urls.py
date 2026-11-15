from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    OrderViewSet,
    ProductViewSet,
    StaffOrderViewSet,
)


app_name = "api"

router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    "products",
    ProductViewSet,
    basename="product",
)
router.register(
    "orders",
    OrderViewSet,
    basename="order",
)
router.register(
    "staff/orders",
    StaffOrderViewSet,
    basename="staff-order",
)

urlpatterns = [
    path("", include(router.urls)),
]