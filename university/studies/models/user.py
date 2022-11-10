import collections
from email.policy import default
from random import choices
from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField


class UserRole:
    ADMIN = "ADMIN"
    CURATOR = "CURATOR"
    STUDENT = "STUDENT"

    RESOLVER = collections.OrderedDict(
        [(ADMIN, "Администратор"), (CURATOR, "Куратор"), (STUDENT, "Студент")]
    )
    CHOICES = RESOLVER.items()


class User(AbstractUser):
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = [(MALE, "Male"), (FEMALE, "Female")]
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    patronymic_name = models.CharField("Отчество", max_length=150)
    gender = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES, default=MALE)
    passport = models.CharField("Серия, номер паспорта", max_length=12, unique=True)
    roles = MultiSelectField(
        "Роли", choices=UserRole.CHOICES, max_length=64
    )
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "patronymic_name",
        "passport",
        "gender",
        "roles",
    ]

    @property
    def is_admin(self):
        return UserRole.ADMIN in self.roles

    @property
    def is_curator(self):
        return UserRole.CURATOR in self.roles

    @property
    def is_student(self):
        return UserRole.STUDENT in self.roles

    class Meta:
        verbose_name = "Участник учебного процесса"
        verbose_name_plural = "Участники учебного процесса"

    def __str__(self):
        return f"{self.first_name} {self.patronymic_name} {self.last_name}"
