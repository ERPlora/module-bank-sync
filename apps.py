from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BankSyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bank_sync'
    label = 'bank_sync'
    verbose_name = _('Bank Reconciliation')

    def ready(self):
        pass
