from ebooks.models import Book
from django.core.files.base import ContentFile
import os

# Create or Get the Uzbek Book
book, created = Book.objects.get_or_create(nationality='uz', defaults={'title': 'Bir Kunda Bir Suhbat'})

book.title = "Bir Kunda Bir Suhbat"
book.detailed_description = """"Bir Kunda Bir Suhbat" — bu shunchaki darslik emas, balki ikki millat vakillarini bog'lovchi noyob ko'prikdir.

Ushbu kitob yapon tilidan umuman xabari yo'q o'quvchini 1 oy ichida kundalik hayotda erkin muloqot qila oladigan darajaga olib chiqishga mo'ljallangan. 
Xuddi shunday, yaponiyalik o'quvchilar uchun ham 1 oy davomida o'zbek tilida kundalik mavzularda gaplasha olish imkoniyatini yaratadi.

Bu kitob JLPT imtihonlari uchun emas, balki jonli va tezkor so'zlashuv uchun maxsus ishlab chiqilgan."""

book.author_name = "Masharipov Ergashboy"
book.author_bio = """O'zbekistonning iqtidorli yoshlaridan biri. Bir vaqtning o'zida 3 ta nufuzli universitetda (JDU, O‘zDJTU, Kyoto Tachibana) tahsil oladi.
Dasturlash, lingvistika va psixologiya sohalari mutaxassisi. "SU Academy" platformasi va ushbu kitob asoschisi."""

book.language = "O'zbek, Yapon"
book.page_count = 135
book.published_year = 2025
book.price = 20000

# Set Image Paths (Relative to MEDIA_ROOT)
book.author_image = 'ebooks/authors/author_ergashboy.jpg'
book.cover_image = 'ebooks/covers/book-cover.png'

book.save()
print(f"Successfully updated book: {book.title}")
