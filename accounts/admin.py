from django.contrib import admin

from .models import Education, Experience, NormalUser, Referee, Skill, User

admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(NormalUser)
admin.site.register(Referee)
admin.site.register(Skill)
admin.site.register(User)
