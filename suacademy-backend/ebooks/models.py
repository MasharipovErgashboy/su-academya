from django.db import models


class Book(models.Model):
    NATIONALITY_CHOICES = (
        ("uz", "Uzbek"),
        ("ja", "Japanese"),
    )

    nationality = models.CharField(
        max_length=2,
        choices=NATIONALITY_CHOICES,
        default="uz"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, verbose_name="Qisqacha tavsif")
    
    # Book Details
    detailed_description = models.TextField(blank=True, verbose_name="Kitob haqida (batafsil)")
    language = models.CharField(max_length=100, default="O'zbek, Yapon", verbose_name="Tillar")
    page_count = models.IntegerField(default=135, verbose_name="Betlar soni")
    published_year = models.IntegerField(default=2025, verbose_name="Nashr yili")
    price = models.IntegerField(default=20000, verbose_name="Narxi (so'm)")

    # Author
    author_name = models.CharField(max_length=255, default="Masharipov Ergashboy", verbose_name="Muallif ismi")
    author_bio = models.TextField(blank=True, verbose_name="Muallif haqida")
    author_image = models.ImageField(upload_to='ebooks/authors/', blank=True, null=True, verbose_name="Muallif rasmi")

    # Files
    pdf_file = models.FileField(upload_to='ebooks/pdfs/')
    cover_image = models.ImageField(upload_to='ebooks/covers/', blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.nationality})"
