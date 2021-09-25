from django.contrib import admin
from .models import Project, Collection, Asset


# Register your models here.
admin.site.register(Project)
admin.site.register(Collection)
admin.site.register(Asset)

