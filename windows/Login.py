from database import Database
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui_py import Ui_LoginWindow


class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self, db: Database):
        super().__init__()
        self.setupUi(self)
        self.db = db

        self.login_btn.clicked.connect(self.authenticate)
        self.guest_btn.clicked.connect(self.continue_as_guest)

    def authenticate(self):
        login = self.login_edit.text().strip()
        password = self.pass_edit.text().strip()

        if not login or not password:
            QMessageBox.critical(self, "Ошибка", "Необходимо заполнить поля логин/пароль")
            return

        user_data = self.db.authenticate(login, password)
        if not user_data:
            QMessageBox.critical(self, "Ошибка", "Неправильно введен логин и/или пароль")
            return

        from .Main import MainWindow
        self.next = MainWindow(self.db, user_data[0])
        self.next.show()
        self.hide()
        self.destroy()

    def continue_as_guest(self):
        user_data = {"user_id": 0,
                     "user_name": "Гость",
                     "role_name": "Гость"}

        from .Main import MainWindow
        self.next = MainWindow(self.db, user_data)
        self.next.show()
        self.hide()
        self.destroy()
