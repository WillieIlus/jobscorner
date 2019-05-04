# import os
#
# import django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobcorner.settings")
# os.environ["DJANGO_SETTINGS_MODULE"] = "jobcorner.settings"
# django.setup()

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from actstream import registry
        # registry.register(self.get_model('Review'), self.get_model('User'), self.get_model('Job'), self.get_model('User'))
        registry.register(self.get_model('User'))
