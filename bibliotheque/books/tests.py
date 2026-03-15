from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from accounts.models import UserProfile
from books.models import Book, Category
from loans.models import Loan


class BookViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Roman')
        self.book = Book.objects.create(
            title='Le Petit Prince', author='Antoine de Saint-Exupéry', isbn='1234567890123',
            category=self.category, total_copies=3, available_copies=3
        )
        self.user = User.objects.create_user(username='lecteur', password='pass12345')
        UserProfile.objects.filter(user=self.user).update(role='lecteur')

    def test_book_list_requires_login(self):
        response = self.client.get(reverse('books:book-list'))
        self.assertEqual(response.status_code, 302)

    def test_search_by_author(self):
        self.client.login(username='lecteur', password='pass12345')
        response = self.client.get(reverse('books:book-list'), {'author': 'Saint'})
        self.assertContains(response, 'Le Petit Prince')


    def test_book_list_is_paginated(self):
        self.client.login(username='lecteur', password='pass12345')
        for index in range(15):
            Book.objects.create(
                title=f'Livre {index}',
                author='Auteur',
                isbn=f'9999999999{index:03d}'[:13],
                category=self.category,
                total_copies=1,
                available_copies=1,
            )
        response = self.client.get(reverse('books:book-list'))
        self.assertTrue(response.context['page_obj'].paginator.num_pages >= 2)


class SeedCommandTests(TestCase):
    def test_seed_command_creates_demo_data(self):
        call_command('seed_bibliotheque', books=10, test_users=3, librarians=2, loans=12)

        self.assertGreaterEqual(Category.objects.count(), 1)
        self.assertGreaterEqual(Book.objects.count(), 10)
        self.assertTrue(User.objects.filter(username='test1').exists())
        self.assertTrue(User.objects.filter(username='biblio1').exists())
        self.assertGreaterEqual(Loan.objects.count(), 1)

        reader = User.objects.get(username='test1')
        self.assertTrue(reader.check_password('t123456'))
