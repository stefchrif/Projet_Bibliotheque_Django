from django.urls import path

from .views import signup_view

app_name = 'accounts'

urlpatterns = [
    path('inscription/', signup_view, name='signup'),
]
