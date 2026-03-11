"""
AI context for the Bank Sync module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Bank Sync

### Models

**BankAccount**
- `name` (CharField): friendly name, e.g. "CaixaBank Cuenta Principal"
- `bank_name` (CharField, optional): bank institution name
- `account_number` (CharField, optional): internal account number
- `iban` (CharField, max 34, optional): IBAN code
- `currency` (CharField, max 3, default `EUR`): ISO 4217 code
- `balance` (Decimal 14,2): current account balance (updated on sync)
- `is_active` (bool, default True)
- Related: `transactions` (BankTransaction set)

**BankTransaction**
- `account` (FK BankAccount, CASCADE, related_name `transactions`)
- `date` (DateField): transaction date
- `description` (CharField, max 255): transaction description from bank
- `amount` (Decimal 14,2): positive = credit (income), negative = debit (outgoing)
- `balance_after` (Decimal 14,2): account balance after this transaction
- `is_reconciled` (bool, default False): whether matched to an expense/invoice
- `reference` (CharField, optional): bank reference code

### Key flows

**Set up a bank account:**
1. Create `BankAccount` with name, IBAN, and initial balance

**Import transactions:**
1. Parse bank statement (CSV/OFX/API)
2. Create `BankTransaction` records linked to the account
3. Update `BankAccount.balance` to current balance

**Reconcile transactions:**
- Match `BankTransaction` to an expense or invoice
- Set `is_reconciled=True` on matched transactions
- Unreconciled transactions: `BankTransaction.objects.filter(account=acc, is_reconciled=False)`

### Relationships
- BankAccount → BankTransaction (one-to-many, related_name `transactions`)
- BankTransaction has no FK to expenses or invoicing — reconciliation is handled by external logic
"""
