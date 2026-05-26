import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize, Qt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
RES_DIR = os.path.join(BASE_DIR, "resources")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)


def _ensure_pixmap(path, size=QSize(120, 100)):
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
