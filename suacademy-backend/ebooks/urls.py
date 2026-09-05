from django.urls import path
from .views import BookDetailAPIView, get_book_pdf

app_name = "ebooks"

urlpatterns = [
    path("detail/", BookDetailAPIView.as_view(), name="book_detail"),
    path("pdf/", get_book_pdf, name="book_pdf"),
]
