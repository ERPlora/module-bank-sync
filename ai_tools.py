"""AI tools for the Bank Sync module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListBankAccounts(AssistantTool):
    name = "list_bank_accounts"
    description = "List bank accounts."
    module_id = "bank_sync"
    required_permission = "bank_sync.view_bankaccount"
    parameters = {"type": "object", "properties": {"is_active": {"type": "boolean"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from bank_sync.models import BankAccount
        qs = BankAccount.objects.all()
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        return {"accounts": [{"id": str(a.id), "name": a.name, "bank_name": a.bank_name, "iban": a.iban, "currency": a.currency, "balance": str(a.balance), "is_active": a.is_active} for a in qs]}


@register_tool
class CreateBankAccount(AssistantTool):
    name = "create_bank_account"
    description = "Create a bank account."
    module_id = "bank_sync"
    required_permission = "bank_sync.add_bankaccount"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}, "bank_name": {"type": "string"},
            "account_number": {"type": "string"}, "iban": {"type": "string"},
            "currency": {"type": "string", "description": "ISO 4217 (e.g., EUR)"},
        },
        "required": ["name", "bank_name"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from bank_sync.models import BankAccount
        a = BankAccount.objects.create(
            name=args['name'], bank_name=args['bank_name'],
            account_number=args.get('account_number', ''), iban=args.get('iban', ''),
            currency=args.get('currency', 'EUR'),
        )
        return {"id": str(a.id), "name": a.name, "created": True}


@register_tool
class ListBankTransactions(AssistantTool):
    name = "list_bank_transactions"
    description = "List bank transactions with filters."
    module_id = "bank_sync"
    required_permission = "bank_sync.view_banktransaction"
    parameters = {
        "type": "object",
        "properties": {
            "account_id": {"type": "string"}, "is_reconciled": {"type": "boolean"},
            "date_from": {"type": "string"}, "date_to": {"type": "string"},
            "limit": {"type": "integer"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from bank_sync.models import BankTransaction
        qs = BankTransaction.objects.select_related('account').all()
        if args.get('account_id'):
            qs = qs.filter(account_id=args['account_id'])
        if 'is_reconciled' in args:
            qs = qs.filter(is_reconciled=args['is_reconciled'])
        if args.get('date_from'):
            qs = qs.filter(date__gte=args['date_from'])
        if args.get('date_to'):
            qs = qs.filter(date__lte=args['date_to'])
        limit = args.get('limit', 20)
        return {
            "transactions": [
                {"id": str(t.id), "date": str(t.date), "description": t.description, "amount": str(t.amount), "is_reconciled": t.is_reconciled, "account": t.account.name}
                for t in qs.order_by('-date')[:limit]
            ]
        }
