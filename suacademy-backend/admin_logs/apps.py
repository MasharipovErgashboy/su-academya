from django.apps import AppConfig


class AdminLogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_logs"
    verbose_name = "Admin Audit Logs"

    def ready(self):
        import admin_logs.signals
