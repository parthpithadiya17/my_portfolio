from django.contrib import admin

from .models import Experience, Project, Skill,ContactMessage,Blog



admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(ContactMessage)
admin.site.register(Blog)

# @admin.register(Blog)
# class BlogAdmin(models.ModelAdmin):
#     list_display = ("title", "created_at", "is_published")
    # prepopulated_fields = {"slug": ("title",)}