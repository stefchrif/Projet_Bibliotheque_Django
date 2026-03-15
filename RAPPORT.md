# Rapport - Projet Gestion d'une Bibliothèque (Django)

## 1) Architecture adoptée
Le projet suit l'architecture standard Django avec séparation en applications métiers :
- **accounts** : gestion des profils utilisateurs et des rôles (lecteur / bibliothécaire).
- **books** : catalogue des livres, catégories, recherche, tri, export CSV et commande de seed.
- **loans** : cycle d'emprunt/retour, filtres avancés, export CSV et tableau de bord statistique.

La configuration globale est centralisée dans `config/settings.py`, `config/urls.py`, `config/wsgi.py` et `config/asgi.py`.

## 2) Fonctionnalités implémentées
### a) Gestion des livres (CRUD)
- Ajout, modification, suppression et affichage des livres.
- Champs gérés : titre, auteur, ISBN (unique), catégorie, année de publication, copies totales, copies disponibles.
- Tri et recherche côté interface.

### b) Gestion des emprunts et retours
- Enregistrement d'un emprunt (lecteur + livre + date de retour prévue).
- Validation d'un retour avec mise à jour automatique :
  - statut de l'emprunt,
  - date de retour effective,
  - disponibilité du livre (+1 copie disponible).
- Affichage visuel du statut : en cours, retourné, en retard.

### c) Authentification et autorisations
- Authentification Django native (`login`, `logout`).
- Inscription dédiée aux lecteurs.
- Contrôle d'accès par rôle :
  - **Bibliothécaire** : gestion complète (livres, catégories, emprunts, dashboard, exports).
  - **Lecteur** : consultation/recherche + ses emprunts uniquement.

### d) Recherche/filtrage avancé
- **Livres** : titre, auteur, catégorie, disponibilité.
- **Emprunts** : lecteur (bibliothécaire), titre du livre, date d'emprunt, date de retour, statut, retards uniquement.

### e) Améliorations réalisées
- Pagination sur les tableaux (livres, catégories, emprunts + listes admin).
- Tableau de bord bibliothécaire (statistiques globales + top livres + derniers emprunts).
- Export CSV du catalogue et des emprunts.
- Seed manuel pour générer des données de démonstration réalistes.

## 3) Choix techniques
- **Django ORM** pour toutes les opérations en base de données.
- **Formulaires Django** (`ModelForm` et `Form`) pour la validation des entrées.
- **Templates Django** + Bootstrap pour l'interface.
- **SQLite** pour la simplicité de déploiement et l'évaluation académique.
- **WhiteNoise** pour la gestion des fichiers statiques en environnement de déploiement simple.

## 4) Qualité et organisation
- Structure modulaire par application.
- Validation métier dans les formulaires (cohérence copies disponibles/total).
- Gestion des permissions par rôle et filtrage sécurisé côté backend.
- Tests unitaires couvrant modèles, vues, pagination, filtres, exports et commande seed.

## 5) Exécution du projet
1. Créer et activer un environnement virtuel.
2. Installer les dépendances (`pip install -r requirements.txt`).
3. Appliquer les migrations (`python manage.py migrate`).
4. (Optionnel) Créer un superutilisateur (`python manage.py createsuperuser`).
5. Lancer le serveur (`python manage.py runserver`).

## 6) Remplissage automatique de la base (seed)
Pour créer rapidement des données de test (livres, catégories, lecteurs, bibliothécaires, emprunts) :

```bash
cd bibliotheque
python manage.py seed_bibliotheque
```

Exemple avec paramètres explicites :

```bash
python manage.py seed_bibliotheque --books 50 --test-users 10 --librarians 2 --loans 100
```

### Données créées par défaut
- ~50 livres marocains.
- Catégories associées.
- Lecteurs `test1`, `test2`, ...
- Bibliothécaires `biblio1`, `biblio2`, ...
- Mot de passe commun : `t123456`
- Emprunts de démonstration avec dates couvrant la période du **01/03/2026** au **15/03/2026**.
