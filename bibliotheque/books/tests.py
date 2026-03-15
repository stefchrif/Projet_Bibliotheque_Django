from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import UserProfile
from books.models import Book, Category


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
