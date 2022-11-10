from django.contrib import admin

from studies.models import EducationGroups, Student

@admin.register(EducationGroups)
class EducationGroupsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "faculty", "count_free_places"]

    def count_free_places(self, obj):
        return 20 - Student.objects.filter(group=obj).count()

    count_free_places.short_description = "Количество свободных мест в группе"
