from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from accounts.models import UserProfile
from books.models import Book, Category
from loans.models import Loan


class LoanModelTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Science')
        self.book = Book.objects.create(
            title='Cosmos', author='Carl Sagan', isbn='1111111111111', category=category, total_copies=1, available_copies=0
        )
        self.reader = User.objects.create_user(username='alice', password='pass12345')
        UserProfile.objects.filter(user=self.reader).update(role='lecteur')

    def test_mark_returned_updates_book(self):
        loan = Loan.objects.create(
            book=self.book,
            reader=self.reader,
            due_date=timezone.now().date() + timedelta(days=7),
        )
        loan.mark_returned()
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)
