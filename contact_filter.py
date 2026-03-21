"""
Фильтр контактных данных в чате сделки.
Блокирует попытки обменяться контактами в обход бота:
- @username
- Телефоны
- Ссылки (http, t.me, wa.me и т.д.)
- Email
"""
import re

# @username (Telegram)
_RE_USERNAME = re.compile(r"@\w{3,}", re.IGNORECASE)

# Телефоны: +7..., 8(9..., +998..., +7 777 и т.д.
_RE_PHONE = re.compile(
    r"(?:\+?\d{1,3}[\s\-\(]*\d[\d\s\-\(\)]{6,14}\d)"
)

# Ссылки: http(s), t.me, wa.me, tg://
_RE_LINK = re.compile(
    r"(?:https?://|t\.me/|tg://|wa\.me/|bit\.ly/|telegram\.me/)\S+",
    re.IGNORECASE,
)

# Email
_RE_EMAIL = re.compile(r"\S+@\S+\.\S+")


def contains_contact(text: str) -> bool:
    """Возвращает True, если текст содержит контактные данные."""
    if _RE_USERNAME.search(text):
        return True
    if _RE_PHONE.search(text):
        return True
    if _RE_LINK.search(text):
        return True
    if _RE_EMAIL.search(text):
        return True
    return False
