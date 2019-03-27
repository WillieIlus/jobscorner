from __future__ import unicode_literals

from django.contrib import admin

from .models import Country, Location


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


admin.site.register(Location, LocationAdmin)
admin.site.register(Country)
