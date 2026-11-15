# Cahier de recettes — Tacos Express

Ce cahier décrit les contrôles fonctionnels à réaliser avant une livraison.
La colonne **Résultat constaté** est à compléter après chaque campagne.

| ID | Fonction | Scénario | Résultat attendu | Résultat constaté |
|---|---|---|---|---|
| REC-01 | Accueil | Ouvrir `/` | La page d'accueil et trois produits maximum s'affichent | À compléter |
| REC-02 | Menu | Ouvrir `/menu/` | Seuls les produits actifs et en stock s'affichent | À compléter |
| REC-03 | Panier | Ajouter un produit | Le produit apparaît avec une quantité égale à 1 | À compléter |
| REC-04 | Panier | Augmenter puis diminuer une quantité | La quantité et le total sont recalculés | À compléter |
| REC-05 | Panier | Supprimer un produit | Le produit disparaît du panier | À compléter |
| REC-06 | Commande | Valider un panier non vide | La commande est créée et le stock diminue | À compléter |
| REC-07 | Commande | Tenter de commander un stock insuffisant | La commande est refusée avec un message d'erreur | À compléter |
| REC-08 | Compte | Créer un compte valide | Le compte rejoint automatiquement le groupe Clients | À compléter |
| REC-09 | Sécurité | Ouvrir le profil sans connexion | Redirection vers la connexion | À compléter |
| REC-10 | Historique | Consulter ses commandes | Seules les commandes du client connecté sont visibles | À compléter |
| REC-11 | API JWT | Envoyer des identifiants valides par POST | Un jeton access et un jeton refresh sont retournés | À compléter |
| REC-12 | API JWT | Appeler `/api/orders/` sans jeton | Réponse HTTP 401 | À compléter |
| REC-13 | Rôles | Créer un produit avec un compte Client | Réponse HTTP 403 | À compléter |
| REC-14 | Rôles | Créer un produit avec un Manager | Réponse HTTP 201 | À compléter |
| REC-15 | Statut | Passer de pending à confirmed | Modification acceptée | À compléter |
| REC-16 | Statut | Passer directement de pending à delivered | Modification refusée | À compléter |

## Commandes de contrôle

```bash
python manage.py check
python manage.py test
python manage.py check --deploy
```

Une anomalie doit contenir : son identifiant, le scénario, le résultat obtenu,
le résultat attendu, une capture éventuelle, sa gravité et sa correction.
