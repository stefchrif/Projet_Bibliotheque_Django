from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import UserProfile
from books.models import Book, Category
from loans.models import Loan


COMMON_PASSWORD = 't123456'
START_DATE = date(2026, 3, 1)
END_DATE = date(2026, 3, 15)


MOROCCAN_BOOKS = [
    ('Le Passé simple', 'Driss Chraïbi', 'Roman marocain'),
    ('La Civilisation, ma Mère!', 'Driss Chraïbi', 'Roman marocain'),
    ('La Boîte à merveilles', 'Ahmed Sefrioui', 'Roman marocain'),
    ('Les Boucs', 'Driss Chraïbi', 'Roman marocain'),
    ('Le Pain nu', 'Mohamed Choukri', 'Roman marocain'),
    ('Le Temps des erreurs', 'Mohamed Choukri', 'Roman marocain'),
    ('Une enfance à Tanger', 'Mohamed Choukri', 'Roman marocain'),
    ('L’Enfant de sable', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('La Nuit sacrée', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('Cette aveuglante absence de lumière', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('Partir', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('Sur ma mère', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('Le Dernier ami', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('Harrouda', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('Moha le fou, Moha le sage', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('Amour sorcier', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('Le Bonheur conjugal', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('La Prière de l’absent', 'Tahar Ben Jelloun', 'Roman marocain'),
    ('Le Journal d’un dégonflé à Casablanca', 'Auteur Marocain', 'Jeunesse'),
    ('Récits de la Médina', 'Auteur Marocain', 'Nouvelles'),
    ('Au pays', 'Abdelkebir Khatibi', 'Roman marocain'),
    ('La Mémoire tatouée', 'Abdelkebir Khatibi', 'Essai'),
    ('Amour bilingue', 'Abdelkebir Khatibi', 'Roman marocain'),
    ('Le Livre du sang', 'Abdelkebir Khatibi', 'Essai'),
    ('Les étoiles de Sidi Moumen', 'Mahi Binebine', 'Roman marocain'),
    ('Le Fou du roi', 'Mahi Binebine', 'Roman marocain'),
    ('Cannibales', 'Mahi Binebine', 'Roman marocain'),
    ('Le Sommeil de l’esclave', 'Mahi Binebine', 'Roman marocain'),
    ('Pollens', 'Mahi Binebine', 'Poésie'),
    ('Le Retour de l’éléphant', 'Mahi Binebine', 'Roman marocain'),
    ('Une année chez les Français', 'Fouad Laroui', 'Roman marocain'),
    ('Les Dents du topographe', 'Fouad Laroui', 'Roman marocain'),
    ('De quel amour blessé', 'Fouad Laroui', 'Roman marocain'),
    ('L’Étrange affaire du pantalon de Dassoukine', 'Fouad Laroui', 'Humour'),
    ('Ce vain combat que tu livres au monde', 'Fouad Laroui', 'Roman marocain'),
    ('L’Oued et le Consul', 'Driss Ksikes', 'Roman marocain'),
    ('Ma boîte noire', 'Abdellah Taïa', 'Roman marocain'),
    ('L’Armée du salut', 'Abdellah Taïa', 'Roman marocain'),
    ('Un pays pour mourir', 'Abdellah Taïa', 'Roman marocain'),
    ('Infidèles', 'Abdellah Taïa', 'Roman marocain'),
    ('Le Jardin des pleurs', 'Abdellah Taïa', 'Roman marocain'),
    ('Hot Maroc', 'Yassin Adnan', 'Roman marocain'),
    ('Le Ciel de Bay City', 'Mourad Bourboune', 'Roman marocain'),
    ('Désorientation', 'Najat El Hachmi', 'Roman marocain'),
    ('Le Harem de la mémoire', 'Fatima Mernissi', 'Sociologie'),
    ('Rêves de femmes', 'Fatima Mernissi', 'Sociologie'),
    ('Le Maroc raconté par ses femmes', 'Fatima Mernissi', 'Sociologie'),
    ('Le Capital social au Maroc', 'Auteur Marocain', 'Économie'),
    ('Histoire du Maroc moderne', 'Auteur Marocain', 'Histoire'),
    ('Casablanca, fragments d’imaginaire', 'Auteur Marocain', 'Culture'),
]


class Command(BaseCommand):
    help = 'Insère des données de démonstration: catégories, livres marocains, utilisateurs de test et emprunts.'

    def add_arguments(self, parser):
        parser.add_argument('--books', type=int, default=50)
        parser.add_argument('--test-users', type=int, default=10)
        parser.add_argument('--librarians', type=int, default=2)
        parser.add_argument('--loans', type=int, default=100)

    @transaction.atomic
    def handle(self, *args, **options):
        books_target = max(options['books'], 1)
        readers_target = max(options['test_users'], 1)
        librarians_target = max(options['librarians'], 1)
        loans_target = max(options['loans'], 1)

        categories_by_name = {}
        books = []

        selected_books = MOROCCAN_BOOKS[:books_target]
        for index, (title, author, category_name) in enumerate(selected_books, start=1):
            category, _ = Category.objects.get_or_create(name=category_name)
            categories_by_name[category_name] = category
            isbn = f'2300000000{index:03d}'[:13]
            book, _ = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': title,
                    'author': author,
                    'category': category,
                    'publication_year': 2000 + (index % 24),
                    'total_copies': 3,
                    'available_copies': 3,
                },
            )
            if book.category_id != category.id:
                book.category = category
                book.save(update_fields=['category'])
            books.append(book)

        readers = []
        for idx in range(1, readers_target + 1):
            username = f'test{idx}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': f'Test{idx}',
                    'last_name': 'Lecteur',
                    'email': f'{username}@example.com',
                },
            )
            if created:
                user.set_password(COMMON_PASSWORD)
                user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if profile.role != UserProfile.ROLE_LECTEUR:
                profile.role = UserProfile.ROLE_LECTEUR
                profile.save(update_fields=['role'])
            readers.append(user)

        for idx in range(1, librarians_target + 1):
            username = f'biblio{idx}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': f'Biblio{idx}',
                    'last_name': 'Gestion',
                    'email': f'{username}@example.com',
                    'is_staff': True,
                },
            )
            updated_fields = []
            if not user.is_staff:
                user.is_staff = True
                updated_fields.append('is_staff')
            if created:
                user.set_password(COMMON_PASSWORD)
                user.save()
            elif updated_fields:
                user.save(update_fields=updated_fields)

            profile, _ = UserProfile.objects.get_or_create(user=user)
            if profile.role != UserProfile.ROLE_BIBLIOTHECAIRE:
                profile.role = UserProfile.ROLE_BIBLIOTHECAIRE
                profile.save(update_fields=['role'])

        combos_existing = set(
            Loan.objects.filter(reader__username__startswith='test')
            .values_list('reader_id', 'book_id', 'loan_date')
        )

        created_loans = 0
        day_span = (END_DATE - START_DATE).days + 1
        day_offsets = [i % day_span for i in range(loans_target * 3)]

        for index, day_offset in enumerate(day_offsets):
            if created_loans >= loans_target:
                break

            reader = readers[index % len(readers)]
            book = books[(index * 3) % len(books)]
            loan_day = START_DATE + timedelta(days=day_offset)
            combo = (reader.id, book.id, loan_day)
            if combo in combos_existing:
                continue

            is_returned = (index % 3 == 0)
            if not is_returned and book.available_copies <= 0:
                continue

            due = min(END_DATE, loan_day + timedelta(days=10))
            loan = Loan.objects.create(
                book=book,
                reader=reader,
                loan_date=loan_day,
                due_date=due,
                status=Loan.STATUS_RETOURNE if is_returned else Loan.STATUS_EN_COURS,
                return_date=(loan_day + timedelta(days=3)) if is_returned else None,
            )

            if not is_returned:
                book.available_copies -= 1
                book.save(update_fields=['available_copies'])

            combos_existing.add(combo)
            created_loans += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seed terminé: {len(categories_by_name)} catégories, {len(books)} livres, '
            f'{len(readers)} lecteurs test, {librarians_target} bibliothécaires, '
            f'{created_loans} emprunts créés. Mot de passe commun: {COMMON_PASSWORD}'
        ))
