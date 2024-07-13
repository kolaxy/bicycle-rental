from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

admin.site.site_header = "br admin panel"


@admin.register(User)
class MainUserAdmin(UserAdmin):
    change_user_password_template = None
    list_display = ("email", "name", "added_at", "id")
    list_filter = ("added_at",)
    search_fields = ("email",)
    ordering = ("-added_at",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ("id",)

    fieldsets = [
        ["User additional data", {"fields": ["id", "name"]}],
        [
            "Authorization",
            {"fields": ["is_superuser", "groups", "user_permissions"]},
        ],
        ["Authentication", {"fields": ["email", "password"]}],
    ]
    add_fieldsets = [
        [
            "Authorization",
            {"fields": ["is_superuser", "groups", "user_permissions"]},
        ],
        ["Authenticated", {"fields": ["email", "password1", "password2"]}],
    ]
