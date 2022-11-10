from typing import Sequence
from django.contrib import admin

from studies.models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["id", "student_user", "group"]
    ordering: Sequence[str] = ["group"]
