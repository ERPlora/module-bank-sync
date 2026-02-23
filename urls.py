from django.urls import path
from . import views

app_name = 'bank_sync'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('transactions/', views.transactions, name='transactions'),
    path('settings/', views.settings, name='settings'),
]
