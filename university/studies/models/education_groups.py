from tabnanny import verbose
from django.db import models


class EducationGroups(models.Model):
    name = models.CharField("Наименование группы", max_length=128, unique=True)
    faculty = models.ForeignKey("Faculty", verbose_name="Направление обучения", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Студенческая группа"
        verbose_name_plural = "Студенческие группы"

    def __str__(self):
        return f'Группа {self.name} на направлении {self.faculty}'