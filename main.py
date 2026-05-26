import os.path
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from utiity import RES_DIR

if __name__ == "__main__":
    from database import Database
    db = Database()
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {font: 14pt "Times New Roman"; 
    color: black;}
    QMainWindow, QDialog {background-color: rgb(255, 255, 255);}
QPushButton {
background-color: #7FFF00;
}
QPushButton:hover {
background-color:#00FA9A;
}
QFrame#ProductFrame {background-color: white; border: 2px solid dark green; color: black;}
QFrame#ProductFrame:hover {background-color: rgb(196, 255, 218)} 

 QLabel {
        background-color: transparent;
        color: black;
    }
    QLabel:hover {
        background-color: transparent;
        color: black;
    }
    
    /* Для картинок в QLabel */
    QLabel[pixmap] {
        background-color: transparent;
    }
    """)
    icon = QIcon(os.path.join(RES_DIR, "Icon.JPG"))
    app.setWindowIcon(icon)
    from windows import LoginWindow
    window = LoginWindow(db)
    window.show()
    app.exec()