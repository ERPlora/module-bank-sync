from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

class BankAccount(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    bank_name = models.CharField(max_length=255, blank=True, verbose_name=_('Bank Name'))
    account_number = models.CharField(max_length=50, blank=True, verbose_name=_('Account Number'))
    iban = models.CharField(max_length=34, blank=True, verbose_name=_('Iban'))
    currency = models.CharField(max_length=3, default='EUR', verbose_name=_('Currency'))
    balance = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Balance'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'bank_sync_bankaccount'

    def __str__(self):
        return self.name


class BankTransaction(HubBaseModel):
    account = models.ForeignKey('BankAccount', on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField(verbose_name=_('Date'))
    description = models.CharField(max_length=255, verbose_name=_('Description'))
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_('Amount'))
    balance_after = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Balance After'))
    is_reconciled = models.BooleanField(default=False, verbose_name=_('Is Reconciled'))
    reference = models.CharField(max_length=100, blank=True, verbose_name=_('Reference'))

    class Meta(HubBaseModel.Meta):
        db_table = 'bank_sync_banktransaction'

    def __str__(self):
        return self.reference

