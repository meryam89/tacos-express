# Bilan de validation — 18 octobre 2026

## Résultats techniques

- `python manage.py check` : réussi, aucune anomalie ;
- `python manage.py test` : 13 tests réussis sur 13 ;
- `python manage.py collectstatic --noinput` : réussi ;
- `python manage.py check --deploy` avec paramètres de production : réussi,
  aucune anomalie.

## Couverture des blocs

| Bloc | État après les travaux | Preuves présentes |
|---|---|---|
| Conception et modélisation | Réalisé | Maquettage et diagrammes préparés séparément |
| Développement | Réalisé | Applications Django, templates et API REST |
| Base de données | Réalisé | Modèles, relations et migrations |
| Sécurité | Réalisé pour le périmètre local/API | CSRF, mots de passe Django, JWT, groupes et permissions |
| Tests et qualité | Validé techniquement | 13 tests automatisés et cahier de recettes |
| Déploiement et DevOps | Préparé, pas encore hébergé | Variables, Gunicorn, WhiteNoise, Procfile et procédure |
| Gestion de projet | Documenté | Découpage, difficultés, solutions, bilan et perspectives |
| Glossaire | Réalisé | `docs/GLOSSAIRE.md` |
