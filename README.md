# Projet Django - Gestion d'une Bibliothèque

## Fonctionnalités
- Authentification des utilisateurs (connexion, déconnexion, inscription lecteur).
- Gestion des rôles : lecteur et bibliothécaire.
- CRUD complet des livres.
- Gestion des catégories de livres.
- Gestion des emprunts et retours.
- Recherche avancée des livres (titre, auteur, catégorie, disponibilité).

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
