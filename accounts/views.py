from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from django.contrib.auth.models import Group

from .forms import ProfileForm, RegistrationForm


def register(request):
    """
    Crée un compte client.
    """

    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        # Récupère le groupe Clients.
        # Si le groupe n'existe pas, Django le crée.
        client_group, created = Group.objects.get_or_create(
            name="Clients"
        )

        # Ajoute le nouvel utilisateur au groupe Clients.
        user.groups.add(client_group)

        messages.success(
            request,
            (
                f"Bienvenue {user.first_name}. "
                "Votre compte a été créé."
            ),
        )

        return redirect("accounts:login")

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )

@login_required
def profile(request):
    """
    Affiche et modifie les informations
    de l'utilisateur connecté.
    """

    form = ProfileForm(
        request.POST or None,
        instance=request.user,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Votre profil a été mis à jour.",
        )

        return redirect("accounts:profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
        },
    )