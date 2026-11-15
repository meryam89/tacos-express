# Préparation du déploiement

## État exact du projet

Le projet fonctionne actuellement en local. Les fichiers nécessaires à une
mise en production sont préparés, mais cela ne constitue pas encore une preuve
de déploiement réel.

## Variables obligatoires

Les valeurs sensibles ne doivent pas être écrites dans Git. Le serveur doit
fournir au minimum :

```text
DJANGO_SECRET_KEY=<clé longue et aléatoire>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<nom-de-domaine>
```

## Procédure générique

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
gunicorn config.wsgi:application
```

## Contrôles avant livraison

- `DEBUG` est désactivé ;
- la clé secrète est uniquement dans l'environnement ;
- `ALLOWED_HOSTS` contient le domaine ;
- HTTPS est actif ;
- les migrations et fichiers statiques sont installés ;
- les tests sont réussis ;
- une sauvegarde de la base est prévue ;
- les journaux ne contiennent ni mot de passe ni jeton JWT ;
- les comptes administrateurs emploient des mots de passe forts.

## Limites

SQLite convient à la démonstration et au développement. Pour un trafic réel,
une base telle que PostgreSQL ou MySQL et une stratégie de sauvegarde doivent
être étudiées. Les images téléversées doivent être stockées durablement par
l'hébergeur ou un service de fichiers dédié.
