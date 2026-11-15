# Gestion de projet — Tacos Express

## 1. Objectif

Créer une application web de restauration permettant à un client de consulter
un catalogue, gérer un panier, commander, créer un compte et suivre ses
commandes. Les employés et managers disposent d'accès adaptés à leur rôle.

## 2. Organisation retenue

Le travail a été conduit de manière incrémentale : chaque fonction a été
ajoutée puis vérifiée avant de passer à la suivante. Le projet a été séparé en
applications Django : `restaurant`, `orders`, `accounts` et `api`.

## 3. Découpage des travaux

| Phase | Travaux réalisés | Livrable |
|---|---|---|
| Analyse | Besoin, acteurs, règles métier et fonctionnalités | Dossier d'analyse |
| Conception | Maquette ordinateur, UML, MCD et architecture | Diagrammes et maquettage |
| Catalogue | Catégories, produits, photos, stock et administration | Menu dynamique |
| Commande | Panier en session, formulaire, total et diminution du stock | Parcours de commande |
| Comptes | Inscription, connexion, profil et historique | Espace client |
| API | Sérialiseurs, endpoints, JWT et permissions | API REST sécurisée |
| Qualité | Tests automatisés et cahier de recettes | Dossier de tests |
| Livraison | Configuration, dépendances et procédure | Préparation au déploiement |

## 4. Difficultés et solutions

| Difficulté rencontrée | Cause | Solution apportée |
|---|---|---|
| Templates introuvables | Mauvais emplacement ou fichier absent | Organisation dans `templates/<application>/` |
| Routes non reconnues | Vue ou namespace absent | Ajout des vues, `app_name` et chemins nommés |
| Panier vide après ajout | Session ou formulaire POST incomplet | Stockage du panier dans `request.session` |
| Identifiants oubliés | Mot de passe non lisible car haché | Réinitialisation sécurisée avec Django |
| Accès API refusé | Jeton ou rôle absent | JWT et groupes Clients, Employes, Managers |
| Configuration sensible | Clé secrète dans les paramètres | Variables d'environnement et fichier d'exemple |

## 5. Choix techniques

- Django fournit l'ORM, l'authentification, les formulaires et l'administration.
- SQLite simplifie le développement et la démonstration locale.
- Le panier est conservé dans la session avant la création d'une commande.
- Une transaction protège la création de commande et la mise à jour du stock.
- JWT protège l'API REST et les permissions limitent les actions selon le rôle.

## 6. Bilan

Le projet répond au parcours principal : consulter, commander et suivre. Il
met en œuvre une architecture en couches, une base relationnelle, une API et
plusieurs mécanismes de sécurité. La procédure de production est préparée mais
un véritable hébergement reste à réaliser et à valider séparément.

## 7. Perspectives

- déploiement sur un hébergement HTTPS ;
- passage éventuel à PostgreSQL ou MySQL en production ;
- paiement en ligne ;
- notifications de changement de statut ;
- adaptation responsive complète pour les smartphones ;
- intégration continue exécutant automatiquement les tests.
