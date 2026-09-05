from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import FileResponse

from drf_yasg.utils import swagger_auto_schema

from .models import Book
from .serializers import BookDetailSerializer


class BookDetailAPIView(APIView):
    """
    GET /ebooks/detail/
    Get available ebook for user's nationality
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["ebooks"])
    def get(self, request):
        user = request.user
        
        # Filter by user's nationality
        nationality = getattr(user, 'nationality', 'uz')
        book = Book.objects.filter(is_active=True, nationality=nationality).first()
        
        if not book:
            return Response(
                {"detail": "Book not found for your region"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BookDetailSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book_pdf(request):
    """
    GET /ebooks/pdf/
    Stream PDF file securely
    """
    user = request.user
    nationality = getattr(user, 'nationality', 'uz')
    
    # Filter by user's nationality
    book = Book.objects.filter(is_active=True, nationality=nationality).first()
    
    if not book or not book.pdf_file:
        return Response(
            {"detail": "PDF not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Open file in binary mode for streaming
    handle = book.pdf_file.open('rb')
    response = FileResponse(handle, content_type='application/pdf')
    
    # Set headers directly on FileResponse
    response['Content-Disposition'] = 'inline; filename="book.pdf"'
    response['X-Content-Type-Options'] = 'nosniff'
    
    return response
