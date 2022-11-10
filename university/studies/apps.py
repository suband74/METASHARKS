from django.apps import AppConfig


class StudiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "studies"
    verbose_name: str = "Обучающий процесс"
