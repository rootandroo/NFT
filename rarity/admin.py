from django.contrib import admin
from .models import Project, Collection, Asset

class CollectionInline(admin.TabularInline):
    model = Collection

class ProjectAdmin(admin.ModelAdmin):
    inlines = [CollectionInline]

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Asset)

