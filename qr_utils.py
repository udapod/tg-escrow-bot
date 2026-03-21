"""Генерация QR-кодов для бота."""
import io
import qrcode
from qrcode.image.pil import PilImage


def generate_qr(data: str) -> io.BytesIO:
    """Генерирует QR-код и возвращает PNG-байты в BytesIO."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
