"""
Bank Reconciliation Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('bank_sync', 'dashboard')
@htmx_view('bank_sync/pages/dashboard.html', 'bank_sync/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('bank_sync', 'accounts')
@htmx_view('bank_sync/pages/accounts.html', 'bank_sync/partials/accounts_content.html')
def accounts(request):
    """Accounts view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('bank_sync', 'transactions')
@htmx_view('bank_sync/pages/transactions.html', 'bank_sync/partials/transactions_content.html')
def transactions(request):
    """Transactions view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('bank_sync', 'settings')
@htmx_view('bank_sync/pages/settings.html', 'bank_sync/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

