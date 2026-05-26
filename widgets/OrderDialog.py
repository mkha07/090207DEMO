import datetime

from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate
from database import Database
from ui_py import Ui_OrderDialog


class OrderDialog(QDialog, Ui_OrderDialog):
    def __init__(self, db: Database, data=None):
        super().__init__()
        self.setupUi(self)

        self.db = db
        self.data = data
        self.load_combos()
        if self.data:
            self.load_data()
            self.setWindowTitle("Редактировать заказ")
        else:
            self.id_lbl.setVisible(False)
            self.id_edit.setVisible(False)
            self.setWindowTitle("Добавить заказ")

        self.connect_btns()

    def load_data(self):
        d = self.data

        self.id_edit.setText(str(d.get("order_id")))

        status_index = self.status_combo.findData(d.get("status_id"))
        self.status_combo.setCurrentIndex(status_index)

        client_index = self.client_combo.findData(d.get("user_id"))
        self.client_combo.setCurrentIndex(client_index)

        self.address_edit.setText(str(d.get("delivery_address")))
        self.order_date.setDate(datetime.date.fromisoformat(str(d.get("order_date"))))
        self.delivery_date.setDate(datetime.date.fromisoformat(str(d.get("delivery_date"))))

    def load_combos(self):
        statuses = self.db.get_statuses()
        for item in statuses:
            self.status_combo.addItem(item.get("status_name"), item.get("status_id"))

        clients = self.db.get_clients()
        for item in clients:
            self.client_combo.addItem(item.get('user_name'), item.get("user_id"))

    def connect_btns(self):
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)
        self.order_date.dateChanged.connect(self.update_min_max_dates)
        self.delivery_date.dateChanged.connect(self.update_min_max_dates)

    def update_min_max_dates(self):
        self.delivery_date.setMinimumDate(self.order_date.date().addDays(1))
        self.order_date.setMaximumDate(self.delivery_date.date())

    def save(self):
        status_id = self.status_combo.currentData()
        client_id = self.client_combo.currentData()
        delivery_address = self.address_edit.text().strip()
        order_date = self.order_date.date().toPyDate()
        delivery_date = self.delivery_date.date().toPyDate()

        if not all((status_id, client_id, delivery_address, order_date, delivery_date)):
            QMessageBox.warning(self, "Ошибка", "Необходимо заполнить все поля отмеченные <*>")
            return

        if self.data:
            order_id = self.data.get("order_id")
            self.db.update_order(order_id, status_id, client_id, delivery_address, order_date, delivery_date)

        else:
            self.db.insert_order(status_id, client_id, delivery_address, order_date, delivery_date)

        self.accept()
