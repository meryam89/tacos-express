from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = "accounts"


urlpatterns = [
    # Création d'un compte
    path(
        "inscription/",
        views.register,
        name="register",
    ),

    # Connexion
    path(
        "connexion/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html"
        ),
        name="login",
    ),

    # Déconnexion
    path(
        "deconnexion/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "profil/",
        views.profile,
        name="profile",
    ),
]