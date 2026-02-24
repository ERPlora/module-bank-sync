from django.contrib import admin

from .models import BankAccount, BankTransaction

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank_name', 'account_number', 'iban', 'currency', 'created_at']
    search_fields = ['name', 'bank_name', 'account_number', 'iban']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'date', 'description', 'amount', 'balance_after', 'created_at']
    search_fields = ['description', 'reference']
    readonly_fields = ['created_at', 'updated_at']

