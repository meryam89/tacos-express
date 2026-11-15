# Glossaire technique

| Terme | Définition dans le projet |
|---|---|
| API | Interface permettant à un logiciel d'échanger des données avec Tacos Express. |
| API REST | API utilisant les méthodes HTTP et des ressources telles que produits et commandes. |
| Authentification | Vérification de l'identité d'un utilisateur. |
| Autorisation | Vérification des actions qu'un utilisateur identifié peut effectuer. |
| CSRF | Attaque consistant à faire envoyer une requête non souhaitée ; Django protège les formulaires avec un jeton CSRF. |
| Django | Framework Python utilisé pour le backend et les pages web. |
| Endpoint | Adresse précise d'une fonction API, par exemple `/api/orders/`. |
| HTTP 200 | Requête réussie. |
| HTTP 201 | Ressource créée avec succès. |
| HTTP 401 | Authentification absente ou invalide. |
| HTTP 403 | Utilisateur identifié mais action interdite. |
| JWT | Jeton signé servant à authentifier les appels à l'API. |
| Migration | Fichier décrivant une évolution de la structure de la base Django. |
| MCD | Représentation des données métier et de leurs relations. |
| ORM | Outil Django transformant les objets Python en requêtes de base de données. |
| Permission | Règle déterminant si un rôle peut exécuter une action. |
| Rôle | Groupe de droits : Clients, Employes ou Managers. |
| Sérialiseur | Composant DRF qui valide et transforme les objets en JSON et inversement. |
| Session | Stockage côté serveur utilisé notamment pour conserver le panier. |
| SQLite | Base de données utilisée par la version actuelle de l'application. |
| Transaction | Ensemble d'opérations validées ou annulées ensemble pour préserver la cohérence. |
| URL nommée | Route Django référencée par un nom stable dans les vues et templates. |
| WhiteNoise | Outil servant les fichiers statiques Django en production simple. |
| WSGI | Interface utilisée pour exécuter Django derrière un serveur tel que Gunicorn. |
