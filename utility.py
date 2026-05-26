import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize, Qt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
RES_DIR = os.path.join(BASE_DIR, "resources")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

# Константы ролей — используются во всём проекте
ROLE_ADMIN = "Администратор"
ROLE_MANAGER = "Менеджер"
ROLE_GUEST = "Гость"
ROLE_CLIENT = "Авторизованный клиент"

STAFF_ROLES = (ROLE_ADMIN, ROLE_MANAGER)


def ensure_pixmap(path, size=QSize(120, 100)):
    """Загружает картинку по пути; если нет — возвращает заглушку."""
    pixmap = None

    if path and os.path.exists(path):
        pixmap = QPixmap(path)

    if not pixmap or pixmap.isNull():
        picture = os.path.join(RES_DIR, "picture.png")
        pixmap = QPixmap(picture)

    if not pixmap.isNull():
        return pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio,
                             Qt.TransformationMode.SmoothTransformation)
    return QPixmap(size)


# Обратная совместимость: старый вариант написания функции
_ensure_pixmap = ensure_pixmap
