from django.contrib import admin

from studies.models import Faculty

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "curator"]