from django.urls import path
from . import views

app_name = 'bank_sync'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('accounts/', views.bank_accounts_list, name='accounts'),
    path('transactions/', views.dashboard, name='transactions'),


    # BankAccount
    path('bank_accounts/', views.bank_accounts_list, name='bank_accounts_list'),
    path('bank_accounts/add/', views.bank_account_add, name='bank_account_add'),
    path('bank_accounts/<uuid:pk>/edit/', views.bank_account_edit, name='bank_account_edit'),
    path('bank_accounts/<uuid:pk>/delete/', views.bank_account_delete, name='bank_account_delete'),
    path('bank_accounts/<uuid:pk>/toggle/', views.bank_account_toggle_status, name='bank_account_toggle_status'),
    path('bank_accounts/bulk/', views.bank_accounts_bulk_action, name='bank_accounts_bulk_action'),

    # BankTransaction
    path('bank_transactions/', views.bank_transactions_list, name='bank_transactions_list'),
    path('bank_transactions/add/', views.bank_transaction_add, name='bank_transaction_add'),
    path('bank_transactions/<uuid:pk>/edit/', views.bank_transaction_edit, name='bank_transaction_edit'),
    path('bank_transactions/<uuid:pk>/delete/', views.bank_transaction_delete, name='bank_transaction_delete'),
    path('bank_transactions/bulk/', views.bank_transactions_bulk_action, name='bank_transactions_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
