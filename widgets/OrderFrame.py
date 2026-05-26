from ui_py import Ui_OrderFrame
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QSize


class OrderFrame(QFrame, Ui_OrderFrame):
    def __init__(self, data, role, on_edit=None, on_select=None):
        super().__init__()
        self.setupUi(self)

        self.selected = False
        self.d = data
        self.role = role
        self._on_edit = on_edit
        self._on_select = on_select

        self.default_style = (
            "QFrame#OrderFrame {background-color: white; border: 2px solid dark green; color: black;}")
        self.selected_style = (
            "QFrame#OrderFrame {background-color: rgb(88, 172, 252); color: white; border: 2px solid dark green;} ")

        if self.role == "Администратор":
            self.default_style += " QFrame#OrderFrame:hover {background-color: rgb(196, 255, 218)} "

        self.setStyleSheet(self.default_style)
        self.load_data()

    def load_data(self):
        d = self.d
        self.id_lbl.setText(str(d.get("order_id")))
        self.status_lbl.setText(str(d.get("status_name")))
        self.address_lbl.setText(str(d.get("delivery_address")))
        self.date_lbl.setText(str(d.get("order_date")))

        self.delivery_date_lbl.setText(str(d.get("delivery_date", "Еще не выбрана")))

    def set_selected(self, selected):
        if selected:
            self.setStyleSheet(self.selected_style)
        else:
            self.setStyleSheet(self.default_style)

    def mousePressEvent(self, a0):
        if self._on_select and self.role == "Администратор" and a0.button() == Qt.MouseButton.LeftButton and not self.selected:
            self._on_select(self)
        super().mousePressEvent(a0)

    def mouseDoubleClickEvent(self, a0):
        if self._on_edit and self.role == "Администратор" and a0.button() == Qt.MouseButton.LeftButton:
            self._on_edit(self.d)
        super().mouseDoubleClickEvent(a0)
