"""Tests for bank_sync views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('bank_sync:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('bank_sync:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('bank_sync:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestBankAccountViews:
    """BankAccount view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('bank_sync:bank_accounts_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('bank_sync:bank_accounts_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('bank_sync:bank_accounts_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('bank_sync:bank_accounts_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('bank_sync:bank_accounts_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('bank_sync:bank_accounts_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('bank_sync:bank_account_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('bank_sync:bank_account_add')
        data = {
            'name': 'New Name',
            'bank_name': 'New Bank Name',
            'account_number': 'New Account Number',
            'iban': 'New Iban',
            'currency': 'New Currency',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, bank_account):
        """Test edit form loads."""
        url = reverse('bank_sync:bank_account_edit', args=[bank_account.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, bank_account):
        """Test editing via POST."""
        url = reverse('bank_sync:bank_account_edit', args=[bank_account.pk])
        data = {
            'name': 'Updated Name',
            'bank_name': 'Updated Bank Name',
            'account_number': 'Updated Account Number',
            'iban': 'Updated Iban',
            'currency': 'Updated Currency',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, bank_account):
        """Test soft delete via POST."""
        url = reverse('bank_sync:bank_account_delete', args=[bank_account.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        bank_account.refresh_from_db()
        assert bank_account.is_deleted is True

    def test_toggle_status(self, auth_client, bank_account):
        """Test toggle active status."""
        url = reverse('bank_sync:bank_account_toggle_status', args=[bank_account.pk])
        original = bank_account.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        bank_account.refresh_from_db()
        assert bank_account.is_active != original

    def test_bulk_delete(self, auth_client, bank_account):
        """Test bulk delete."""
        url = reverse('bank_sync:bank_accounts_bulk_action')
        response = auth_client.post(url, {'ids': str(bank_account.pk), 'action': 'delete'})
        assert response.status_code == 200
        bank_account.refresh_from_db()
        assert bank_account.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('bank_sync:bank_accounts_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestBankTransactionViews:
    """BankTransaction view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('bank_sync:bank_transactions_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('bank_sync:bank_transactions_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('bank_sync:bank_transactions_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('bank_sync:bank_transactions_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('bank_sync:bank_transactions_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('bank_sync:bank_transactions_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('bank_sync:bank_transaction_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('bank_sync:bank_transaction_add')
        data = {
            'date': '2025-01-15',
            'description': 'New Description',
            'amount': '100.00',
            'balance_after': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, bank_transaction):
        """Test edit form loads."""
        url = reverse('bank_sync:bank_transaction_edit', args=[bank_transaction.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, bank_transaction):
        """Test editing via POST."""
        url = reverse('bank_sync:bank_transaction_edit', args=[bank_transaction.pk])
        data = {
            'date': '2025-01-15',
            'description': 'Updated Description',
            'amount': '100.00',
            'balance_after': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, bank_transaction):
        """Test soft delete via POST."""
        url = reverse('bank_sync:bank_transaction_delete', args=[bank_transaction.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        bank_transaction.refresh_from_db()
        assert bank_transaction.is_deleted is True

    def test_bulk_delete(self, auth_client, bank_transaction):
        """Test bulk delete."""
        url = reverse('bank_sync:bank_transactions_bulk_action')
        response = auth_client.post(url, {'ids': str(bank_transaction.pk), 'action': 'delete'})
        assert response.status_code == 200
        bank_transaction.refresh_from_db()
        assert bank_transaction.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('bank_sync:bank_transactions_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('bank_sync:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('bank_sync:settings')
        response = client.get(url)
        assert response.status_code == 302

