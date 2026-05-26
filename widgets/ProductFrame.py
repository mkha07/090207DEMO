import os.path

from ui_py import Ui_ProductFrame
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QSize
from utility import ensure_pixmap as _ensure_pixmap, IMAGES_DIR, ROLE_ADMIN


class ProductFrame(QFrame, Ui_ProductFrame):
    def __init__(self, data, role, on_edit=None, on_select=None):
        super().__init__()
        self.setupUi(self)

        self.selected = False
        self.data = data
        self.role = role
        self._on_edit = on_edit
        self._on_select = on_select

        self.default_style = "QFrame#ProductFrame {background-color: white; border: 2px solid darkgreen; color: black;}"
        self.selected_style = "QFrame#ProductFrame {background-color: rgb(88, 172, 252); color: white; border: 2px solid darkgreen;}"
        self.high_discount_style = "QFrame#ProductFrame {background-color: #2E8B57; color: white; border: 2px solid darkgreen;}"

        if self.role == ROLE_ADMIN:
            self.default_style += " QFrame#ProductFrame:hover {background-color: rgb(196, 255, 218)}"
            self.high_discount_style += " QFrame#ProductFrame:hover {background-color: rgb(196, 255, 218)}"

        self.setStyleSheet(self.default_style)
        self.load_data()

    def load_data(self):
        img_name = self.data.get("photo", "")
        if img_name:
            pixmap = _ensure_pixmap(os.path.join(IMAGES_DIR, img_name), QSize(180, 150))
        else:
            pixmap = _ensure_pixmap("", QSize(180, 150))

        self.img_lbl.setPixmap(pixmap)

        self.name_cat_lbl.setText(f"{self.data.get('category_name', '')} | {self.data.get('type_name', '')}")
        self.desc_lbl.setText(f"Описание товара: {self.data.get('description', '')}")
        self.manuf_lbl.setText(f"Производитель: {self.data.get('manufacturer_name', '')}")
        self.supplier_lbl.setText(f"Поставщик: {self.data.get('supplier_name', '')}")

        old_price = self.data.get('price', 0)
        self.price_lbl.setText(f"Цена: {old_price:.2f} руб.")
        self.unit_lbl.setText(f"Единица измерения: {self.data.get('unit', '')}")
        self.stock_lbl.setText(f"Количество на складе: {self.data.get('stock', 0)}")

        discount = self.data.get('discount', 0)
        self.discount_lbl.setText(f"{discount}%")
        self.discount_lbl.setStyleSheet("background-color: rgb(255, 147, 0); color: rgb(255, 255, 255);")

        if discount > 0:
            new_price = float(old_price) * (1 - float(discount) / 100)
            self.price_lbl.setText(
                f"Цена: <span style='color:red; text-decoration: line-through'>{old_price:.2f}</span> "
                f"<span style='color:black; font-weight:bold'>{new_price:.2f}</span> руб."
            )
            self.price_lbl.setTextFormat(Qt.TextFormat.RichText)

            if discount > 15 and not self.selected:
                self.setStyleSheet(self.high_discount_style)

        if self.data.get('stock', 0) <= 0:
            self.stock_lbl.setStyleSheet("color: cyan")

    def set_selected(self, selected):
        self.selected = selected
        discount = self.data.get('discount', 0)
        if selected:
            self.setStyleSheet(self.selected_style)
        elif discount > 15:
            self.setStyleSheet(self.high_discount_style)
        else:
            self.setStyleSheet(self.default_style)

    def mousePressEvent(self, a0):
        if self._on_select and self.role == ROLE_ADMIN and a0.button() == Qt.MouseButton.LeftButton and not self.selected:
            self._on_select(self)
        super().mousePressEvent(a0)

    def mouseDoubleClickEvent(self, a0):
        if self._on_edit and self.role == ROLE_ADMIN and a0.button() == Qt.MouseButton.LeftButton:
            self._on_edit(self.data)
        super().mouseDoubleClickEvent(a0)
