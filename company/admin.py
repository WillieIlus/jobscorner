from django.contrib import admin

from .models import Company, CompanyImage, OpeningHours, ClosingRules, Vote

admin.site.register(Company)
admin.site.register(CompanyImage)
admin.site.register(OpeningHours)
admin.site.register(ClosingRules)
admin.site.register(Vote)
