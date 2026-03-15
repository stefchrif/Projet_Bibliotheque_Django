from django.contrib import admin

from .models import Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 20


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'available_copies')
    search_fields = ('title', 'author', 'isbn')
    list_per_page = 20
