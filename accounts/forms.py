from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """
    Formulaire de création d'un compte client.
    """

    email = forms.EmailField(
        required=True,
        label="Adresse e-mail",
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

        labels = {
            "username": "Nom d'utilisateur",
            "first_name": "Prénom",
            "last_name": "Nom",
        }

    def clean_email(self):
        """
        Vérifie que l'adresse e-mail
        n'est pas déjà utilisée.
        """

        email = self.cleaned_data["email"].lower()

        if User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Cette adresse e-mail est déjà utilisée."
            )

        return email


class ProfileForm(forms.ModelForm):
    """
    Formulaire permettant à un utilisateur
    de modifier ses informations personnelles.
    """

    email = forms.EmailField(
        required=True,
        label="Adresse e-mail",
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

        labels = {
            "username": "Nom d'utilisateur",
            "first_name": "Prénom",
            "last_name": "Nom",
        }

    def clean_email(self):
        """
        Vérifie que l'adresse e-mail n'est pas
        utilisée par un autre compte.
        """

        email = self.cleaned_data["email"].lower()

        email_exists = User.objects.filter(
            email__iexact=email,
        ).exclude(
            id=self.instance.id,
        ).exists()

        if email_exists:
            raise forms.ValidationError(
                "Cette adresse e-mail est déjà utilisée."
            )

        return email