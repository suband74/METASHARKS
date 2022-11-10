from django.contrib import admin

from studies.models import Subjects

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]