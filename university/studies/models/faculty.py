from django.db import models
from django.conf import settings


class Faculty(models.Model):
    name = models.CharField("Название направления обучения", max_length=128)
    subjects_of_study = models.ManyToManyField(
        "Subjects", verbose_name="Предмет обучения", related_name="subjects"
    )
    curator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Куратор",
        related_name="curator",
    )

    class Meta:
        verbose_name = "Направление обучения"
        verbose_name_plural = "Направления обучения"

    def __str__(self):
        return self.name
