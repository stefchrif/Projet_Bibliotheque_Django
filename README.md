# Projet Django - Gestion d'une Bibliothèque

## Fonctionnalités
- Authentification des utilisateurs (connexion, déconnexion, inscription lecteur).
- Gestion des rôles : lecteur et bibliothécaire.
- CRUD complet des livres.
- Gestion des catégories de livres.
- Gestion des emprunts et retours.
- Filtres avancés sur les emprunts (lecteur, livre, date emprunt, date retour, statut).
- Recherche avancée des livres (titre, auteur, catégorie, disponibilité).
- Pagination activée sur les tableaux (livres, emprunts, catégories) et sur les listes admin.
- Gestion visuelle des retards (badge + filtre dédié).
- Export CSV du catalogue et des emprunts (côté bibliothécaire).
- Tableau de bord bibliothécaire avec statistiques (livres, lecteurs, emprunts, retards, top livres).

## Stack
- Django 5.x
- SQLite
- Templates Django + Bootstrap

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd bibliotheque
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Déploiement (important pour le CSS de l'admin)
Si l'admin apparaît sans style, c'est généralement un problème de fichiers statiques non servis.

1. Définir les variables d'environnement de production:
```bash
export DJANGO_DEBUG=false
export DJANGO_ALLOWED_HOSTS="ton-domaine.com,www.ton-domaine.com"
export DJANGO_SECRET_KEY="une-cle-secrete-forte"
```

2. Collecter les fichiers statiques:
```bash
cd bibliotheque
python manage.py collectstatic --noinput
```

3. Configurer ton serveur web (Nginx/Apache) pour servir l'URL `/static/` depuis le dossier `bibliotheque/staticfiles/`.

> Le projet est configuré avec `STATIC_ROOT = BASE_DIR / "staticfiles"` pour ce scénario.

## Comptes et permissions
- Les utilisateurs avec rôle `bibliothecaire` peuvent gérer les livres, catégories et emprunts.
- Les utilisateurs avec rôle `lecteur` peuvent consulter/rechercher les livres et voir leurs emprunts.

## Structure
- `bibliotheque/config` : configuration globale du projet.
- `bibliotheque/accounts` : profils, rôles, inscription.
- `bibliotheque/books` : catalogue, CRUD et recherche.
- `bibliotheque/loans` : emprunts et retours.

## Tests
```bash
cd bibliotheque
python manage.py test
```


## Dépannage 404 sur `/static/admin/...`
Si tu vois des erreurs 404 comme `/static/admin/css/base.css` ou `/static/admin/js/jquery.init.js`, c'est normal qu'ils **n'existent pas dans ton repo**: ce sont des fichiers fournis par Django, copiés pendant `collectstatic`.

Checklist:
1. Installer les dépendances (incluant WhiteNoise):
```bash
pip install -r requirements.txt
```
2. Lancer la collecte des statics à chaque déploiement:
```bash
cd bibliotheque
python manage.py collectstatic --noinput
```
3. Redémarrer le service web (Gunicorn/uWSGI/etc.).

Avec la configuration actuelle, WhiteNoise peut servir automatiquement les statics en production si ton reverse proxy ne les sert pas directement.


## Erreur 404 sur `/accounts/login/`
Le projet utilise l'URL française `/comptes/login/` pour l'authentification.
Pour compatibilité avec des liens par défaut Django (ou anciens liens), un alias `/accounts/login/` est aussi actif dans les URLs.

Si tu as toujours une 404 après mise à jour, redémarre le service applicatif.


## Erreur 405 sur `/accounts/logout/`
Depuis les versions récentes de Django, la déconnexion via la vue intégrée nécessite une requête **POST** (et non GET).
Le bouton "Déconnexion" du projet envoie maintenant un formulaire POST avec token CSRF.

Note: une route explicite `/accounts/logout/` (et `/comptes/logout/`) a aussi été ajoutée pour accepter GET et POST afin d'éviter les erreurs 405 selon les environnements.

Si ton serveur affiche encore une 405, fais:
1. `git pull`
2. redémarre le service applicatif (Gunicorn/uWSGI)
3. vide le cache navigateur puis reteste.


## Gestion du rôle bibliothécaire dans l'admin
Le rôle n'apparaît pas directement dans le formulaire standard `Utilisateurs` de Django tant qu'on n'ajoute pas le profil.
Le projet inclut maintenant:
- un écran dédié `User profiles` dans l'admin,
- et un encart `Profil` sur la page d'édition d'un utilisateur (après création) pour choisir `Lecteur` ou `Bibliothécaire`.

⚠️ Sur l'écran "Ajouter un utilisateur", Django crée d'abord l'utilisateur (username + mot de passe), puis tu cliques sur l'utilisateur créé pour définir le rôle dans `Profil`.


## Données de démonstration (seed manuel)
Tu peux peupler automatiquement la base avec des données de test marocaines via:

```bash
cd bibliotheque
python manage.py seed_bibliotheque
```

Cette commande crée:
- environ 50 livres (auteurs/titres marocains),
- des catégories,
- des lecteurs `test1`, `test2`, `test3`, ...
- des bibliothécaires `biblio1`, `biblio2`, ...
- un mot de passe commun: `t123456`,
- des emprunts de démo (par défaut 100) avec dates entre le `01/03/2026` et le `15/03/2026`.

Options utiles:
```bash
python manage.py seed_bibliotheque --books 50 --test-users 10 --librarians 2 --loans 100
```
