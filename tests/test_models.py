"""Tests for bank_sync models."""
import pytest
from django.utils import timezone

from bank_sync.models import BankAccount, BankTransaction


@pytest.mark.django_db
class TestBankAccount:
    """BankAccount model tests."""

    def test_create(self, bank_account):
        """Test BankAccount creation."""
        assert bank_account.pk is not None
        assert bank_account.is_deleted is False

    def test_str(self, bank_account):
        """Test string representation."""
        assert str(bank_account) is not None
        assert len(str(bank_account)) > 0

    def test_soft_delete(self, bank_account):
        """Test soft delete."""
        pk = bank_account.pk
        bank_account.is_deleted = True
        bank_account.deleted_at = timezone.now()
        bank_account.save()
        assert not BankAccount.objects.filter(pk=pk).exists()
        assert BankAccount.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, bank_account):
        """Test default queryset excludes deleted."""
        bank_account.is_deleted = True
        bank_account.deleted_at = timezone.now()
        bank_account.save()
        assert BankAccount.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, bank_account):
        """Test toggling is_active."""
        original = bank_account.is_active
        bank_account.is_active = not original
        bank_account.save()
        bank_account.refresh_from_db()
        assert bank_account.is_active != original


@pytest.mark.django_db
class TestBankTransaction:
    """BankTransaction model tests."""

    def test_create(self, bank_transaction):
        """Test BankTransaction creation."""
        assert bank_transaction.pk is not None
        assert bank_transaction.is_deleted is False

    def test_str(self, bank_transaction):
        """Test string representation."""
        assert str(bank_transaction) is not None
        assert len(str(bank_transaction)) > 0

    def test_soft_delete(self, bank_transaction):
        """Test soft delete."""
        pk = bank_transaction.pk
        bank_transaction.is_deleted = True
        bank_transaction.deleted_at = timezone.now()
        bank_transaction.save()
        assert not BankTransaction.objects.filter(pk=pk).exists()
        assert BankTransaction.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, bank_transaction):
        """Test default queryset excludes deleted."""
        bank_transaction.is_deleted = True
        bank_transaction.deleted_at = timezone.now()
        bank_transaction.save()
        assert BankTransaction.objects.filter(hub_id=hub_id).count() == 0


