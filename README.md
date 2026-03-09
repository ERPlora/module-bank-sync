# Bank Reconciliation

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `bank_sync` |
| **Version** | `1.0.0` |
| **Icon** | `card-outline` |
| **Dependencies** | None |

## Models

### `BankAccount`

BankAccount(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, bank_name, account_number, iban, currency, balance, is_active)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `bank_name` | CharField | max_length=255, optional |
| `account_number` | CharField | max_length=50, optional |
| `iban` | CharField | max_length=34, optional |
| `currency` | CharField | max_length=3 |
| `balance` | DecimalField |  |
| `is_active` | BooleanField |  |

### `BankTransaction`

BankTransaction(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, account, date, description, amount, balance_after, is_reconciled, reference)

| Field | Type | Details |
|-------|------|---------|
| `account` | ForeignKey | → `bank_sync.BankAccount`, on_delete=CASCADE |
| `date` | DateField |  |
| `description` | CharField | max_length=255 |
| `amount` | DecimalField |  |
| `balance_after` | DecimalField |  |
| `is_reconciled` | BooleanField |  |
| `reference` | CharField | max_length=100, optional |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `BankTransaction` | `account` | `bank_sync.BankAccount` | CASCADE | No |

## URL Endpoints

Base path: `/m/bank_sync/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `accounts/` | `accounts` | GET |
| `transactions/` | `transactions` | GET |
| `bank_accounts/` | `bank_accounts_list` | GET |
| `bank_accounts/add/` | `bank_account_add` | GET/POST |
| `bank_accounts/<uuid:pk>/edit/` | `bank_account_edit` | GET |
| `bank_accounts/<uuid:pk>/delete/` | `bank_account_delete` | GET/POST |
| `bank_accounts/<uuid:pk>/toggle/` | `bank_account_toggle_status` | GET |
| `bank_accounts/bulk/` | `bank_accounts_bulk_action` | GET/POST |
| `bank_transactions/` | `bank_transactions_list` | GET |
| `bank_transactions/add/` | `bank_transaction_add` | GET/POST |
| `bank_transactions/<uuid:pk>/edit/` | `bank_transaction_edit` | GET |
| `bank_transactions/<uuid:pk>/delete/` | `bank_transaction_delete` | GET/POST |
| `bank_transactions/bulk/` | `bank_transactions_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `bank_sync.view_bankaccount` | View Bankaccount |
| `bank_sync.add_bankaccount` | Add Bankaccount |
| `bank_sync.change_bankaccount` | Change Bankaccount |
| `bank_sync.view_banktransaction` | View Banktransaction |
| `bank_sync.reconcile_transaction` | Reconcile Transaction |
| `bank_sync.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_bankaccount`, `change_bankaccount`, `reconcile_transaction`, `view_bankaccount`, `view_banktransaction`
- **employee**: `add_bankaccount`, `view_bankaccount`, `view_banktransaction`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Accounts | `card-outline` | `accounts` | No |
| Transactions | `list-outline` | `transactions` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_bank_accounts`

List bank accounts.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_active` | boolean | No |  |

### `create_bank_account`

Create a bank account.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes |  |
| `bank_name` | string | Yes |  |
| `account_number` | string | No |  |
| `iban` | string | No |  |
| `currency` | string | No | ISO 4217 (e.g., EUR) |

### `list_bank_transactions`

List bank transactions with filters.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `account_id` | string | No |  |
| `is_reconciled` | boolean | No |  |
| `date_from` | string | No |  |
| `date_to` | string | No |  |
| `limit` | integer | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  bank_sync/
    css/
    js/
  icons/
    icon.svg
templates/
  bank_sync/
    pages/
      accounts.html
      bank_account_add.html
      bank_account_edit.html
      bank_accounts.html
      bank_transaction_add.html
      bank_transaction_edit.html
      bank_transactions.html
      dashboard.html
      index.html
      settings.html
      transactions.html
    partials/
      accounts_content.html
      bank_account_add_content.html
      bank_account_edit_content.html
      bank_accounts_content.html
      bank_accounts_list.html
      bank_transaction_add_content.html
      bank_transaction_edit_content.html
      bank_transactions_content.html
      bank_transactions_list.html
      dashboard_content.html
      panel_bank_account_add.html
      panel_bank_account_edit.html
      panel_bank_transaction_add.html
      panel_bank_transaction_edit.html
      settings_content.html
      transactions_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
