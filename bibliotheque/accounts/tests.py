from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import UserProfile


class RoleBasedLoginRedirectTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username='readerlogin', password='pass12345')
        UserProfile.objects.filter(user=self.reader).update(role='lecteur')

        self.librarian = User.objects.create_user(username='bibliologin', password='pass12345')
        UserProfile.objects.filter(user=self.librarian).update(role='bibliothecaire')

    def test_reader_login_without_next_redirects_to_books(self):
        response = self.client.post(reverse('login'), {
            'username': 'readerlogin',
            'password': 'pass12345',
        })
        self.assertRedirects(response, reverse('books:book-list'))

    def test_librarian_login_without_next_redirects_to_dashboard(self):
        response = self.client.post(reverse('login'), {
            'username': 'bibliologin',
            'password': 'pass12345',
        })
        self.assertRedirects(response, reverse('loans:dashboard'))

    def test_librarian_login_with_next_keeps_next_priority(self):
        response = self.client.post(
            f"{reverse('login')}?next={reverse('books:book-list')}",
            {'username': 'bibliologin', 'password': 'pass12345'},
        )
        self.assertRedirects(response, reverse('books:book-list'))
