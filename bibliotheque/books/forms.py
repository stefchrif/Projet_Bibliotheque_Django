from django import forms

from .models import Book, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'publication_year', 'total_copies', 'available_copies']

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total_copies')
        available = cleaned_data.get('available_copies')
        if total is not None and available is not None and available > total:
            raise forms.ValidationError('Les copies disponibles ne peuvent pas dépasser le total.')
        return cleaned_data


class BookSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Titre')
    author = forms.CharField(required=False, label='Auteur')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Catégorie')
    available = forms.NullBooleanField(required=False, label='Disponible uniquement')
