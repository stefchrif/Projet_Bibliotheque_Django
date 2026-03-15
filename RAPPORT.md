# Rapport - Projet Gestion d'une Bibliothèque (Django)

## 1) Architecture adoptée
Le projet suit l'architecture standard Django avec séparation en applications métiers :
- **accounts** : gestion des profils utilisateurs et des rôles (lecteur / bibliothécaire).
- **books** : catalogue des livres, catégories, recherche avancée et opérations CRUD.
- **loans** : cycle d'emprunt et de retour, avec mise à jour automatique de la disponibilité.

La configuration globale est centralisée dans `config/settings.py`, `config/urls.py`, `config/wsgi.py` et `config/asgi.py`.

## 2) Fonctionnalités implémentées
### a. Gestion des livres (CRUD)
- Ajout d'un livre.
- Modification d'un livre.
- Suppression d'un livre.
- Affichage de la liste des livres.

Champs gérés : titre, auteur, ISBN (unique), catégorie, année de publication, nombre total d'exemplaires, exemplaires disponibles.

### b. Gestion des emprunts et retours
- Enregistrement d'un emprunt (lecteur + livre + date de retour prévue).
- Validation d'un retour avec mise à jour automatique :
  - statut de l'emprunt,
  - date de retour effective,
  - disponibilité du livre (+1 exemplaire disponible).

### c. Authentification et autorisations
- Authentification Django native (`login`, `logout`).
- Inscription dédiée aux lecteurs.
- Contrôle d'accès par rôle :
  - Bibliothécaire : accès aux opérations de gestion.
  - Lecteur : accès consultation/recherche + ses emprunts.

### d. Recherche avancée
Filtres disponibles :
- titre,
- auteur,
- catégorie,
- disponibilité.

## 3) Choix techniques
- **Django ORM** pour toutes les opérations base de données.
- **Formulaires Django** (`ModelForm` et `Form`) pour la validation des entrées.
- **Templates Django** + Bootstrap pour l'interface.
- **SQLite** pour la simplicité de déploiement et l'évaluation académique.

## 4) Qualité et organisation
- Structure modulaire par application.
- Validation métier dans les formulaires (cohérence copies disponibles/total).
- Tests unitaires de base sur des cas critiques : recherche et retour d'emprunt.

## 5) Exécution du projet
1. Créer et activer un environnement virtuel.
2. Installer les dépendances (`pip install -r requirements.txt`).
3. Appliquer les migrations (`python manage.py migrate`).
4. Créer un superutilisateur.
5. Lancer le serveur (`python manage.py runserver`).
