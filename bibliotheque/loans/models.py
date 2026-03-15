from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from books.models import Book


class Loan(models.Model):
    STATUS_EN_COURS = 'en_cours'
    STATUS_RETOURNE = 'retourne'
    STATUS_CHOICES = [
        (STATUS_EN_COURS, 'En cours'),
        (STATUS_RETOURNE, 'Retourné'),
    ]

    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='loans')
    reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_EN_COURS)

    class Meta:
        ordering = ['-loan_date']

    def __str__(self):
        return f'Emprunt {self.book.title} par {self.reader.username}'

    def mark_returned(self):
        if self.status == self.STATUS_RETOURNE:
            return
        self.status = self.STATUS_RETOURNE
        self.return_date = timezone.now().date()
        self.save(update_fields=['status', 'return_date'])
        self.book.available_copies += 1
        self.book.save(update_fields=['available_copies'])
