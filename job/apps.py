from django.apps import AppConfig
from django.db.models.signals import post_migrate

from company.signals import handlers

class JobConfig(AppConfig):
    name = 'job'
    verbose_name = 'Job'

    def ready(self):
        post_migrate.connect(handlers.create_notice_types, sender=self)

