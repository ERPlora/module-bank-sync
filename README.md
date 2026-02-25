# Bank Reconciliation Module

Bank account sync and transaction reconciliation.

## Features

- Bank account management with name, bank, account number, and IBAN
- Multi-currency support per bank account
- Real-time balance tracking per account
- Transaction recording with date, description, amount, and reference
- Balance-after tracking on each transaction
- Transaction reconciliation workflow
- Activate/deactivate bank accounts independently

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Bank Reconciliation > Settings**

## Usage

Access via: **Menu > Bank Reconciliation**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/bank_sync/dashboard/` | Overview of bank account balances and reconciliation status |
| Accounts | `/m/bank_sync/accounts/` | Manage bank accounts |
| Transactions | `/m/bank_sync/transactions/` | Browse and reconcile bank transactions |
| Settings | `/m/bank_sync/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `BankAccount` | Bank account with name, bank name, account number, IBAN, currency, and balance |
| `BankTransaction` | Bank transaction with date, description, amount, balance after, reconciliation status, and reference |

## Permissions

| Permission | Description |
|------------|-------------|
| `bank_sync.view_bankaccount` | View bank accounts |
| `bank_sync.add_bankaccount` | Create new bank accounts |
| `bank_sync.change_bankaccount` | Edit existing bank accounts |
| `bank_sync.view_banktransaction` | View bank transactions |
| `bank_sync.reconcile_transaction` | Reconcile bank transactions |
| `bank_sync.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
