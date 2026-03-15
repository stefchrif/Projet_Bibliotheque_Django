from django.urls import path

from . import views

app_name = 'loans'

urlpatterns = [
    path('', views.loan_list, name='loan-list'),
    path('nouveau/', views.loan_create, name='loan-create'),
    path('<int:pk>/retour/', views.loan_return, name='loan-return'),
]
