from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.utils import is_bibliothecaire

from .forms import BookForm, BookSearchForm, CategoryForm
from .models import Book, Category


@login_required
def book_list(request):
    books = Book.objects.select_related('category').all()
    form = BookSearchForm(request.GET or None)
    if form.is_valid():
        if form.cleaned_data.get('title'):
            books = books.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data.get('author'):
            books = books.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data.get('category'):
            books = books.filter(category=form.cleaned_data['category'])
        available = form.cleaned_data.get('available')
        if available is True:
            books = books.filter(available_copies__gt=0)
        elif available is False:
            books = books.filter(available_copies=0)

    return render(request, 'books/book_list.html', {'books': books, 'search_form': form})


@login_required
@user_passes_test(is_bibliothecaire)
def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('books:book-list')
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Ajouter un livre'})


@login_required
@user_passes_test(is_bibliothecaire)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('books:book-list')
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Modifier le livre'})


@login_required
@user_passes_test(is_bibliothecaire)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('books:book-list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


@login_required
@user_passes_test(is_bibliothecaire)
def category_list(request):
    categories = Category.objects.all()
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('books:category-list')
    return render(request, 'books/category_list.html', {'categories': categories, 'form': form})
