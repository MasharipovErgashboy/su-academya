# ebooks/utils.py
from django.conf import settings


def get_nationality_from_request(request) -> str:
    """
    Frontend nationality tanlaganidan keyin har requestda yuboradi.
    Tavsiya: Header => X-Nationality: uz | jp
    """
    nat = (request.headers.get("X-Nationality") or "").strip().lower()
    if nat in ("uz", "jp"):
        return nat
    return "uz"


def build_signed_url(object_key: str) -> str:
    """
    Bu FUNKSIYANI keyin S3/Cloud signed url bilan almashtirasan.
    Hozircha: BOOKS_PUBLIC_BASE_URL bo'lsa -> public url yasaydi.
    """
    base = getattr(settings, "BOOKS_PUBLIC_BASE_URL", "").strip()
    if base:
        return f"{base.rstrip('/')}/{object_key.lstrip('/')}"
    return object_key
