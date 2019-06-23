from django.contrib import admin

from .models import Type, Item, Service, Price

admin.site.register(Type)
admin.site.register(Item)
admin.site.register(Service)
admin.site.register(Price)
