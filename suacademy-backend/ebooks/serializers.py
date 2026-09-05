from rest_framework import serializers
from .models import Book


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "nationality",
            "title",
            "description",
            "detailed_description",
            "language",
            "page_count",
            "published_year",
            "price",
            "author_name",
            "author_bio",
            "author_image",
            "pdf_file",
            "cover_image",
            "is_active",
            "created_at"
        )
