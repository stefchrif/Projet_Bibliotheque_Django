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
