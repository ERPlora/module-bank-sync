    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'bank_sync'
    MODULE_NAME = _('Bank Reconciliation')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'card-outline'
    MODULE_DESCRIPTION = _('Bank account sync and transaction reconciliation')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'finance'

    MENU = {
        'label': _('Bank Reconciliation'),
        'icon': 'card-outline',
        'order': 49,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Accounts'), 'icon': 'card-outline', 'id': 'accounts'},
{'label': _('Transactions'), 'icon': 'list-outline', 'id': 'transactions'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'bank_sync.view_bankaccount',
'bank_sync.add_bankaccount',
'bank_sync.change_bankaccount',
'bank_sync.view_banktransaction',
'bank_sync.reconcile_transaction',
'bank_sync.manage_settings',
    ]
