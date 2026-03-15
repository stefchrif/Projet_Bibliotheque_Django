import csv

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.utils import is_bibliothecaire

from .forms import BookForm, BookSearchForm, CategoryForm
from .models import Book, Category


def _apply_book_filters(books, form):
    if not form.is_valid():
        return books
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
    return books


@login_required
def book_list(request):
    books = Book.objects.select_related('category').all()
    form = BookSearchForm(request.GET or None)
    books = _apply_book_filters(books, form)

    sort = request.GET.get('sort', 'title')
    sort_map = {
        'title': 'title',
        '-title': '-title',
        'author': 'author',
        '-author': '-author',
        'available': '-available_copies',
    }
    books = books.order_by(sort_map.get(sort, 'title'))

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'books/book_list.html',
        {'books': page_obj, 'search_form': form, 'page_obj': page_obj, 'selected_sort': sort},
    )


@login_required
@user_passes_test(is_bibliothecaire)
def book_export_csv(request):
    books = Book.objects.select_related('category').all()
    form = BookSearchForm(request.GET or None)
    books = _apply_book_filters(books, form)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="livres.csv"'
    writer = csv.writer(response)
    writer.writerow(['Titre', 'Auteur', 'ISBN', 'Catégorie', 'Copies totales', 'Copies disponibles'])
    for book in books:
        writer.writerow([book.title, book.author, book.isbn, book.category.name, book.total_copies, book.available_copies])
    return response


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
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'books/category_list.html',
        {'categories': page_obj, 'form': form, 'page_obj': page_obj},
    )
