from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)


class IsManagerOrReadOnly(BasePermission):
    """
    Autorise tout le monde à consulter.

    Seuls les managers et les superutilisateurs
    peuvent créer, modifier ou supprimer.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return (
            request.user.is_superuser
            or request.user.groups.filter(
                name="Managers"
            ).exists()
        )


class IsEmployeeOrManager(BasePermission):
    """
    Autorise uniquement :

    - les employés ;
    - les managers ;
    - les superutilisateurs.
    """

    def has_permission(self, request, view):
        # Refuse les visiteurs non connectés.
        if not request.user.is_authenticated:
            return False

        # Le superutilisateur possède tous les droits.
        if request.user.is_superuser:
            return True

        # Vérifie l'appartenance à l'un des deux groupes.
        return request.user.groups.filter(
            name__in=[
                "Employes",
                "Managers",
            ]
        ).exists()