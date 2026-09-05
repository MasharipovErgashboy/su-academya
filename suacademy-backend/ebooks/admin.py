from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "nationality",
        "is_active",
        "created_at",
    )
    list_filter = ("nationality", "is_active")
    search_fields = ("title", "description")
