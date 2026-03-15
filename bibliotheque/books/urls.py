from django.urls import path

from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book-list'),
    path('ajouter/', views.book_create, name='book-create'),
    path('<int:pk>/modifier/', views.book_update, name='book-update'),
    path('<int:pk>/supprimer/', views.book_delete, name='book-delete'),
    path('categories/', views.category_list, name='category-list'),
]
