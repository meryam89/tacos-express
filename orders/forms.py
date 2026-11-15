from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    """
    Formulaire utilisé pour récupérer
    les coordonnées de livraison du client.
    """

    class Meta:
        model = Order

        # Champs affichés au client
        fields = [
            "customer_name",
            "email",
            "phone",
            "address",
            "city",
            "postal_code",
            "delivery_instructions",
        ]
        labels = {
            "delivery_instructions": (
                "Choix du Tiramisu XXL "
                "et instructions de livraison"
            ),
        }

        # Personnalisation des champs HTML
        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "placeholder": "Votre nom complet",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "exemple@email.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "06 00 00 00 00",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Numéro et nom de rue",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "placeholder": "Votre ville",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "placeholder": "Code postal",
                }
            ),
            "delivery_instructions": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Choix Tiramisu XXL : Oreo, Spéculoos, "
                        "M&M’s, Daim ou Schokobon. "
                        "Ajoutez aussi vos instructions de livraison."
                    ),
                    "rows": 4,
                }
            ),
        }