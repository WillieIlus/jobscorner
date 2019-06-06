from django.apps import AppConfig
from django.db.models.signals import post_migrate

from company.signals import handlers


class CompanyConfig(AppConfig):
    name = 'company'
    verbose_name = 'company'

    def ready(self):
        post_migrate.connect(handlers.create_notice_types, sender=self)
