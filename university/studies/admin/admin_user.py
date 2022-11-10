from django.contrib import admin

from studies.models import User


class RolesFilter(admin.ChoicesFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_kwarg = "%s__contains" % field_path
        self.lookup_val = params.get(self.lookup_kwarg)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "last_name", "first_name", "patronymic_name", "passport", "roles", "gender"]
    search_fields = ["last_name", "passport"]
    list_filter = [
        "is_active",
        "is_staff",
        "is_superuser",
        ("roles", RolesFilter),  # MultiSelectField,
    ]
    fieldsets = (
        [None, {"fields": ["username", "password"]}],
        [
            ("Personal info"),
            {
                "fields": [
                    "last_name",
                    "first_name",
                    "patronymic_name",
                    "passport",
                    "roles",
                ]
            },
        ],
        [
            ("Permissions"),
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ],
            },
        ],
        [("Important dates"), {"fields": ("last_login", "date_joined")}],
    )
    add_fieldsets = [
        [None, {"fields": ["username", "password1", "password2"]}],
        [
            ("Personal info"),
            {
                "fields": [
                    "last_name",
                    "first_name",
                    "patronymic_name",
                    "passport",
                    "roles",
                ]
            },
        ],
        [
            ("Permissions"),
            {
                "fields": ["is_active", "is_staff", "is_superuser", "groups"],
            },
        ],
    ]
