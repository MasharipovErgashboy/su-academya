from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "01. Users"

    def ready(self):
        from django.contrib import admin
        admin.site.site_header = "SU Academya Administration"
        admin.site.site_title = "SU Academya Admin"
        admin.site.index_title = "SU Academya Management Panel"
