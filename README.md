# Tacos Express

Application web Django de commande et de livraison de nuit. Elle permet de
consulter le catalogue, gérer un panier, passer une commande, suivre son statut
et administrer les produits. Une API REST sécurisée par JWT est également
disponible.

## Technologies

- Python et Django ;
- Django REST Framework et SimpleJWT ;
- HTML, CSS et templates Django ;
- SQLite pour la version actuelle ;
- Gunicorn et WhiteNoise pour la préparation à la production.

## Installation locale

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

L'application est accessible à l'adresse `http://127.0.0.1:8000/`.

## Tests automatisés

```bash
python manage.py check
python manage.py test
```

Les tests couvrent notamment l'inscription, le panier, la création d'une
commande, la diminution du stock, l'isolation des commandes, JWT et les rôles.

## Préparation à la production

1. Copier `.env.example` vers `.env` et remplacer les valeurs.
2. Exporter les variables d'environnement sur le serveur.
3. Exécuter `python manage.py migrate`.
4. Exécuter `python manage.py collectstatic --noinput`.
5. Vérifier avec `python manage.py check --deploy`.
6. Lancer avec `gunicorn config.wsgi:application`.

Le serveur `runserver` est réservé au développement. Un déploiement réel doit
également employer HTTPS, un serveur ou une plateforme d'hébergement, des
sauvegardes et une base de données adaptée à la production.

## Documentation

Les documents de recette, gestion de projet, déploiement et glossaire sont
disponibles dans le dossier `docs/`.
