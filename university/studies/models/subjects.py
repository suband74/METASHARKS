from django.db import models


class Subjects(models.Model):
    name = models.CharField("Название предмета", max_length=128)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name
