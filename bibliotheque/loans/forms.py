from django import forms
from django.contrib.auth.models import User

from books.models import Book

from .models import Loan


class LoanCreateForm(forms.ModelForm):
    reader = forms.ModelChoiceField(queryset=User.objects.all(), label='Lecteur')
    book = forms.ModelChoiceField(queryset=Book.objects.filter(available_copies__gt=0), label='Livre')

    class Meta:
        model = Loan
        fields = ['reader', 'book', 'due_date']
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}


class LoanReturnForm(forms.Form):
    confirm = forms.BooleanField(label='Confirmer le retour')


class LoanFilterForm(forms.Form):
    reader = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Lecteur')
    book_title = forms.CharField(required=False, label='Nom du livre')
    loan_date = forms.DateField(required=False, label='Date emprunt', widget=forms.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(required=False, label='Date retour', widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(
        required=False,
        label='Statut',
        choices=[('', 'Tous')] + Loan.STATUS_CHOICES,
    )

    overdue_only = forms.BooleanField(required=False, label='Retards uniquement')
