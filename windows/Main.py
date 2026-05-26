import os
from database import Database
from PyQt6.QtWidgets import QMainWindow, QLabel, QMessageBox
from PyQt6.QtCore import QSize
from ui_py import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, db: Database, user_data):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.user_data = user_data

        self.current_view = "Товары"
        self.selected_card = None
        self.dialog_opened = False
        self.setup_interface()
        self.setup_combos()
        self.load_grid()

    def setup_interface(self):
        self.back_btn.clicked.connect(self.go_back)
        self.add_btn.clicked.connect(self.add)
        self.del_btn.clicked.connect(self.delete)
        self.products_btn.clicked.connect(self.view_products)
        self.orders_btn.clicked.connect(self.view_orders)
        self.supplier_combo.currentIndexChanged.connect(self.load_grid)
        self.sort_combo.currentIndexChanged.connect(self.load_grid)
        self.search_edit.textChanged.connect(self.load_grid)

        role = self.user_data.get("role_name", "Гость")
        username = self.user_data.get("user_name", "Гость")
        self.username_label.setText(f"{username} ({role})")

        self.products_btn.setVisible(role in ('Администратор', 'Менеджер'))
        self.orders_btn.setVisible(role in ('Администратор', 'Менеджер'))
        self.filter_widget.setVisible(role in ('Администратор', 'Менеджер'))
        self.control_panel.setVisible(role == "Администратор")
        from utiity import RES_DIR, _ensure_pixmap
        logo = os.path.join(RES_DIR, "Icon.png")
        pixmap = _ensure_pixmap(logo, QSize(100, 100))
        self.logo_label.setPixmap(pixmap)

    def go_back(self):
        from .Login import LoginWindow
        self.next = LoginWindow(self.db)
        self.next.show()
        self.hide()
        self.destroy()

    def setup_combos(self):
        self.supplier_combo.addItem("Все поставщики", 0)
        suppliers = self.db.get_suppliers()
        for item in suppliers:
            self.supplier_combo.addItem(item.get("supplier_name"), item.get("supplier_id"))

        self.supplier_combo.setCurrentIndex(0)

        self.sort_combo.addItem("По названию (А-я)", 0)
        self.sort_combo.addItem("По названию (Я-а)", 1)
        self.sort_combo.addItem("По количеству на складе, восх.", 2)
        self.sort_combo.addItem("По количеству на складе, убыв.", 3)
        self.sort_combo.setCurrentIndex(0)

    def _clear_selection(self, except_card=None):
        for i in range(self.card_grid.count()):
            item = self.card_grid.itemAt(i)
            if item and item.widget():
                card = item.widget()
                if card != except_card and hasattr(card, "set_selected"):
                    card.set_selected(False)

    def load_grid(self):
        role = self.user_data.get("role_name", "Гость")
        while self.card_grid.count():
            item = self.card_grid.takeAt(0)
            if item and item.widget():
                widget = item.widget()
                widget.deleteLater()

        self.selected_card = None
        if self.current_view == "Заказы":
            from widgets.OrderFrame import OrderFrame
            card_class = OrderFrame
            data = self.db.get_orders()

        else:
            from widgets.ProductFrame import ProductFrame
            card_class = ProductFrame
            srch = None
            supplier_id = None
            sort_by = "type_name"
            sort_order = "asc"
            if role in ('Администратор', 'Менеджер'):
                srch = self.search_edit.text().strip()
                supplier_id = self.supplier_combo.currentData()
                sort_index = self.sort_combo.currentData()
                sort_dict = {0: ("type_name", "asc"),
                             1: ("type_name", "desc"),
                             2: ("stock", "asc"),
                             3: ("stock", "desc")}
                sort_by, sort_order = sort_dict.get(sort_index, ("type_name", "asc"))

            data = self.db.get_products(srch, supplier_id, sort_by, sort_order)
        if not data:
            self.card_grid.addWidget(QLabel("Отсутсвует информация"), 0, 0)
            return

        COLUMNS = 1

        for i, row in enumerate(data):
            card = card_class(row, role, self.edit_card if role == 'Администратор' else None,
                              self.select_card if role == 'Администратор' else None)
            self.card_grid.addWidget(card, i // COLUMNS, i % COLUMNS)

    def edit_card(self, data):
        role = self.user_data.get("role_name", "Гость")
        if role != 'Администратор':
            QMessageBox.critical(self, "Ошибка", "У Вас недостаточно прав, чтобы выполнить эту операцию")
            return
        if self.dialog_opened:
            QMessageBox.critical(self, "Ошибка", "Нельзя открывть несколько окон добаления/редактирования")
            return
        if self.current_view == "Заказы":
            from widgets.OrderDialog import OrderDialog
            dialog = OrderDialog(self.db, data)
            self.dialog_opened = True
            if dialog.exec():
                QMessageBox.information(self, "Успех", f"Заказ №{data.get('order_id')} обновлен")
                self.load_grid()
            self.dialog_opened = False

        else:
            from widgets.ProductDialog import ProductDialog
            dialog = ProductDialog(self.db, data)
            self.dialog_opened = True
            if dialog.exec():
                QMessageBox.information(self, "Успех", f"Товар №{data.get('product_id')} обновлен")
                self.load_grid()
            self.dialog_opened = False

    def select_card(self, card):
        role = self.user_data.get("role_name", "Гость")
        if role != 'Администратор':
            QMessageBox.critical(self, "Ошибка", "У Вас недостаточно прав, чтобы выполнить эту операцию")
            return
        if card == self.selected_card:
            card.set_selected(False)
            self.selected_card = None
        else:
            self._clear_selection(card)
            card.set_selected(True)
            self.selected_card = card

    def add(self):
        role = self.user_data.get("role_name", "Гость")
        if role != 'Администратор':
            QMessageBox.critical(self, "Ошибка", "У Вас недостаточно прав, чтобы выполнить эту операцию")
            return
        if self.dialog_opened:
            QMessageBox.critical(self, "Ошибка", "Нельзя открывть несколько окон добаления/редактирования")
            return
        if self.current_view == "Заказы":
            from widgets.OrderDialog import OrderDialog
            dialog = OrderDialog(self.db)
            self.dialog_opened = True
            if dialog.exec():
                QMessageBox.information(self, "Успех", "Новый заказ добавлен")
                self.load_grid()
            self.dialog_opened = False
        else:
            from widgets.ProductDialog import ProductDialog
            dialog = ProductDialog(self.db)
            self.dialog_opened = True
            if dialog.exec():
                QMessageBox.information(self, "Успех", "Новый товар добавлен")
                self.load_grid()
            self.dialog_opened = False

    def delete(self):
        role = self.user_data.get("role_name", "Гость")
        if role != 'Администратор':
            QMessageBox.critical(self, "Ошибка", "У Вас недостаточно прав, чтобы выполнить эту операцию")
            return
        if self.selected_card is None:
            QMessageBox.warning(self, "Внимание", "Необходимо сначала выбрать карточку")
            return
        if self.current_view == "Заказы":
            order_id = self.selected_card.d.get("order_id")
            msg = QMessageBox(self)
            msg.setWindowTitle("Внимание!")
            msg.setText("Вы уверены что хотите удалить данный товар?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setIcon(QMessageBox.Icon.Warning)
            if msg.exec() == msg.StandardButton.Yes:
                self.db.del_order(order_id)
                self.load_grid()
                QMessageBox.information(self, 'Успех', "Заказ успешно удален")
        else:
            product_id = self.selected_card.d.get("product_id")
            if self.db.is_product_in_order(product_id):
                QMessageBox.critical(self, "Ошибка", "Нельзя удалить товар, который присутствует в заказе,")
                return
            msg = QMessageBox(self)
            msg.setWindowTitle("Внимание!")
            msg.setText("Вы уверены что хотите удалить данный товар?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setIcon(QMessageBox.Icon.Warning)
            if msg.exec() == msg.StandardButton.Yes:
                self.db.del_product(product_id)
                self.load_grid()
                QMessageBox.information(self, 'Успех', "Товар успешно удален")

    def view_products(self):
        self.supplier_combo.setCurrentIndex(0)
        self.sort_combo.setCurrentIndex(0)
        self.search_edit.setText("")
        role = self.user_data.get("role_name", "Гость")
        self.filter_widget.setVisible(role in ('Администратор', 'Менеджер'))
        self.current_view = "Товары"
        self.load_grid()

    def view_orders(self):
        self.filter_widget.setVisible(False)
        self.current_view = "Заказы"
        self.load_grid()
