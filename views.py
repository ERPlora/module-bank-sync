"""
Bank Reconciliation Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import BankAccount, BankTransaction

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('bank_sync', 'dashboard')
@htmx_view('bank_sync/pages/index.html', 'bank_sync/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_bank_accounts': BankAccount.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_bank_transactions': BankTransaction.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# BankAccount
# ======================================================================

BANK_ACCOUNT_SORT_FIELDS = {
    'name': 'name',
    'is_active': 'is_active',
    'balance': 'balance',
    'bank_name': 'bank_name',
    'account_number': 'account_number',
    'iban': 'iban',
    'created_at': 'created_at',
}

def _build_bank_accounts_context(hub_id, per_page=10):
    qs = BankAccount.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'bank_accounts': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_bank_accounts_list(request, hub_id, per_page=10):
    ctx = _build_bank_accounts_context(hub_id, per_page)
    return django_render(request, 'bank_sync/partials/bank_accounts_list.html', ctx)

@login_required
@with_module_nav('bank_sync', 'accounts')
@htmx_view('bank_sync/pages/bank_accounts.html', 'bank_sync/partials/bank_accounts_content.html')
def bank_accounts_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = BankAccount.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(bank_name__icontains=search_query) | Q(account_number__icontains=search_query) | Q(iban__icontains=search_query))

    order_by = BANK_ACCOUNT_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'is_active', 'balance', 'bank_name', 'account_number', 'iban']
        headers = ['Name', 'Is Active', 'Balance', 'Bank Name', 'Account Number', 'Iban']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='bank_accounts.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='bank_accounts.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'bank_sync/partials/bank_accounts_list.html', {
            'bank_accounts': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'bank_accounts': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def bank_account_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        bank_name = request.POST.get('bank_name', '').strip()
        account_number = request.POST.get('account_number', '').strip()
        iban = request.POST.get('iban', '').strip()
        currency = request.POST.get('currency', '').strip()
        balance = request.POST.get('balance', '0') or '0'
        is_active = request.POST.get('is_active') == 'on'
        obj = BankAccount(hub_id=hub_id)
        obj.name = name
        obj.bank_name = bank_name
        obj.account_number = account_number
        obj.iban = iban
        obj.currency = currency
        obj.balance = balance
        obj.is_active = is_active
        obj.save()
        return _render_bank_accounts_list(request, hub_id)
    return django_render(request, 'bank_sync/partials/panel_bank_account_add.html', {})

@login_required
def bank_account_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BankAccount, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.bank_name = request.POST.get('bank_name', '').strip()
        obj.account_number = request.POST.get('account_number', '').strip()
        obj.iban = request.POST.get('iban', '').strip()
        obj.currency = request.POST.get('currency', '').strip()
        obj.balance = request.POST.get('balance', '0') or '0'
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_bank_accounts_list(request, hub_id)
    return django_render(request, 'bank_sync/partials/panel_bank_account_edit.html', {'obj': obj})

@login_required
@require_POST
def bank_account_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BankAccount, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_bank_accounts_list(request, hub_id)

@login_required
@require_POST
def bank_account_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BankAccount, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_bank_accounts_list(request, hub_id)

@login_required
@require_POST
def bank_accounts_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = BankAccount.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_bank_accounts_list(request, hub_id)


# ======================================================================
# BankTransaction
# ======================================================================

BANK_TRANSACTION_SORT_FIELDS = {
    'reference': 'reference',
    'account': 'account',
    'is_reconciled': 'is_reconciled',
    'balance_after': 'balance_after',
    'amount': 'amount',
    'date': 'date',
    'created_at': 'created_at',
}

def _build_bank_transactions_context(hub_id, per_page=10):
    qs = BankTransaction.objects.filter(hub_id=hub_id, is_deleted=False).order_by('reference')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'bank_transactions': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'reference',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_bank_transactions_list(request, hub_id, per_page=10):
    ctx = _build_bank_transactions_context(hub_id, per_page)
    return django_render(request, 'bank_sync/partials/bank_transactions_list.html', ctx)

@login_required
@with_module_nav('bank_sync', 'accounts')
@htmx_view('bank_sync/pages/bank_transactions.html', 'bank_sync/partials/bank_transactions_content.html')
def bank_transactions_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'reference')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = BankTransaction.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(description__icontains=search_query) | Q(reference__icontains=search_query))

    order_by = BANK_TRANSACTION_SORT_FIELDS.get(sort_field, 'reference')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['reference', 'account', 'is_reconciled', 'balance_after', 'amount', 'date']
        headers = ['Reference', 'BankAccount', 'Is Reconciled', 'Balance After', 'Amount', 'Date']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='bank_transactions.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='bank_transactions.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'bank_sync/partials/bank_transactions_list.html', {
            'bank_transactions': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'bank_transactions': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def bank_transaction_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        date = request.POST.get('date') or None
        description = request.POST.get('description', '').strip()
        amount = request.POST.get('amount', '0') or '0'
        balance_after = request.POST.get('balance_after', '0') or '0'
        is_reconciled = request.POST.get('is_reconciled') == 'on'
        reference = request.POST.get('reference', '').strip()
        obj = BankTransaction(hub_id=hub_id)
        obj.date = date
        obj.description = description
        obj.amount = amount
        obj.balance_after = balance_after
        obj.is_reconciled = is_reconciled
        obj.reference = reference
        obj.save()
        return _render_bank_transactions_list(request, hub_id)
    return django_render(request, 'bank_sync/partials/panel_bank_transaction_add.html', {})

@login_required
def bank_transaction_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BankTransaction, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.date = request.POST.get('date') or None
        obj.description = request.POST.get('description', '').strip()
        obj.amount = request.POST.get('amount', '0') or '0'
        obj.balance_after = request.POST.get('balance_after', '0') or '0'
        obj.is_reconciled = request.POST.get('is_reconciled') == 'on'
        obj.reference = request.POST.get('reference', '').strip()
        obj.save()
        return _render_bank_transactions_list(request, hub_id)
    return django_render(request, 'bank_sync/partials/panel_bank_transaction_edit.html', {'obj': obj})

@login_required
@require_POST
def bank_transaction_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BankTransaction, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_bank_transactions_list(request, hub_id)

@login_required
@require_POST
def bank_transactions_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = BankTransaction.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_bank_transactions_list(request, hub_id)


@login_required
@permission_required('bank_sync.manage_settings')
@with_module_nav('bank_sync', 'settings')
@htmx_view('bank_sync/pages/settings.html', 'bank_sync/partials/settings_content.html')
def settings_view(request):
    return {}

