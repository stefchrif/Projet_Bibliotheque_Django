from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comptes/', include('django.contrib.auth.urls')),  # URL FR principale
    path('accounts/', include('django.contrib.auth.urls')),  # Alias compatibilité
    path('utilisateurs/', include('accounts.urls')),
    path('livres/', include('books.urls')),
    path('emprunts/', include('loans.urls')),
    path('', RedirectView.as_view(pattern_name='books:book-list', permanent=False)),
]
