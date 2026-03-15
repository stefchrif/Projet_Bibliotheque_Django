from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
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


class LoanViewPaginationTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Histoire')
        self.reader = User.objects.create_user(username='reader2', password='pass12345')
        UserProfile.objects.filter(user=self.reader).update(role='lecteur')

        for index in range(15):
            book = Book.objects.create(
                title=f'Book {index}',
                author='Auteur',
                isbn=f'8888888888{index:03d}'[:13],
                category=category,
                total_copies=1,
                available_copies=0,
            )
            Loan.objects.create(
                book=book,
                reader=self.reader,
                due_date=timezone.now().date() + timedelta(days=7),
            )

    def test_loan_list_is_paginated_for_reader(self):
        self.client.login(username='reader2', password='pass12345')
        response = self.client.get(reverse('loans:loan-list'))
        self.assertTrue(response.context['page_obj'].paginator.num_pages >= 2)


class LoanFilterTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Roman')
        self.reader1 = User.objects.create_user(username='testreader1', password='pass12345')
        self.reader2 = User.objects.create_user(username='testreader2', password='pass12345')
        self.librarian = User.objects.create_user(username='biblio', password='pass12345')

        UserProfile.objects.filter(user=self.reader1).update(role='lecteur')
        UserProfile.objects.filter(user=self.reader2).update(role='lecteur')
        UserProfile.objects.filter(user=self.librarian).update(role='bibliothecaire')

        book1 = Book.objects.create(
            title='Livre Atlas', author='Auteur A', isbn='7000000000001', category=category, total_copies=2, available_copies=1
        )
        book2 = Book.objects.create(
            title='Livre Rif', author='Auteur B', isbn='7000000000002', category=category, total_copies=2, available_copies=2
        )

        Loan.objects.create(
            book=book1,
            reader=self.reader1,
            loan_date=timezone.datetime(2026, 3, 10).date(),
            due_date=timezone.datetime(2026, 3, 15).date(),
            status=Loan.STATUS_EN_COURS,
        )
        Loan.objects.create(
            book=book2,
            reader=self.reader2,
            loan_date=timezone.datetime(2026, 3, 9).date(),
            due_date=timezone.datetime(2026, 3, 14).date(),
            return_date=timezone.datetime(2026, 3, 11).date(),
            status=Loan.STATUS_RETOURNE,
        )

    def test_librarian_can_filter_by_status(self):
        self.client.login(username='biblio', password='pass12345')
        response = self.client.get(reverse('loans:loan-list'), {'status': Loan.STATUS_RETOURNE})
        loans = response.context['loans']
        self.assertEqual(loans.paginator.count, 1)
        self.assertContains(response, 'Livre Rif')

    def test_librarian_can_filter_by_reader(self):
        self.client.login(username='biblio', password='pass12345')
        response = self.client.get(reverse('loans:loan-list'), {'reader': self.reader1.id})
        self.assertContains(response, 'Livre Atlas')
        self.assertNotContains(response, 'Livre Rif')

    def test_reader_cannot_see_others_even_with_reader_filter(self):
        self.client.login(username='testreader1', password='pass12345')
        response = self.client.get(reverse('loans:loan-list'), {'reader': self.reader2.id})
        self.assertContains(response, 'Livre Atlas')
        self.assertNotContains(response, 'Livre Rif')
