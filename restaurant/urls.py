from django.urls import path

from . import views


# Namespace utilisé dans les templates :
# restaurant:home et restaurant:menu
app_name = "restaurant"


urlpatterns = [
    # Page d'accueil
    path(
        "",
        views.home,
        name="home",
    ),

    # Page présentant tous les produits
    path(
        "menu/",
        views.menu,
        name="menu",
    ),
]