from django.apps import AppConfig
from django.apps import AppConfig
from django.db.models.signals import post_migrate

from company.signals import handlers

class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = 'Blog Post'

    def ready(self):
        post_migrate.connect(handlers.create_notice_types, sender=self)
