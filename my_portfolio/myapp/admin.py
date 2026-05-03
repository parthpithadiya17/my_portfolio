from django.contrib import admin

from .models import Experience, Project, Skill,ContactMessage


admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(ContactMessage)
