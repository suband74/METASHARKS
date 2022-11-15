from django.db import models
from django.conf import settings


class Student(models.Model):
    student_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Студент",
        related_name="student",
    )
    group = models.ForeignKey(
        "EducationGroups",
        on_delete=models.CASCADE,
        verbose_name="Группа",
        related_name="edu_group",
    )
    email = models.CharField(
        max_length=120,
        verbose_name="Электронная почта",
        default="test@test.mail.ru"
    )
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return f"Студент {self.student_user} группа {self.group}"