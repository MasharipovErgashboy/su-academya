import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO


def generate_qr_png(qr_item):
    """
    QRCodeItem uchun PNG rasm generatsiya qiladi
    """
    qr_url = f"{settings.FRONTEND_URL}/qr/{qr_item.code}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    file_name = f"qr_{qr_item.code}.png"
    qr_item.image.save(file_name, ContentFile(buffer.getvalue()), save=False)
