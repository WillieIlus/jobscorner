from django.apps import AppConfig
from django.db.models.signals import post_migrate

from company.signals import handlers

class ReviewsConfig(AppConfig):
    name = 'reviews'
    verbose_name = 'Review'

    def ready(self):
        post_migrate.connect(handlers.create_notice_types, sender=self)

