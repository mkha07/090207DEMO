import os.path

from PyQt6.QtGui import QPixmap
from pathlib import Path
from database import Database
from ui_py import Ui_ProductDialog
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QSize
from utiity import _ensure_pixmap, IMAGES_DIR


class ProductDialog(QDialog, Ui_ProductDialog):
    def __init__(self, db: Database, data=None):
        super().__init__()
        self.setupUi(self)

        self.db = db
        self.data = data
        self.cleared_img = False
        self.old_img_name = None
        self.new_img_path = None

        self.load_combos()
        self.img_lbl.setPixmap(_ensure_pixmap("", QSize(180, 150)))
        if self.data:
            self.load_data()
            self.setWindowTitle("Редактировать товар")
        else:
            self.label_2.setVisible(False)
            self.id_edit.setVisible(False)
            self.setWindowTitle("Добавить товар")

        self.connect_btns()

    def load_data(self):
        d = self.data
        self.old_img_name = d.get("photo", "")
        old_image_path = os.path.join(IMAGES_DIR, self.old_img_name)
        self.img_lbl.setPixmap(_ensure_pixmap(old_image_path, QSize(180, 150)))

        self.id_edit.setText(str(d.get("product_id")))

        type_index = self.type_combo.findData(d.get("type_id"))
        self.type_combo.setCurrentIndex(type_index)

        cat_index = self.cat_combo.findData(d.get("category_id"))
        self.cat_combo.setCurrentIndex(cat_index)

        self.desc_edit.setText(str(d.get("description", "")))

        manuf_index = self.manuf_combo.findData(d.get("manufacturer_id"))
        self.manuf_combo.setCurrentIndex(manuf_index)

        supplier_index = self.supplier_combo.findData(d.get("supplier_id"))
        self.supplier_combo.setCurrentIndex(supplier_index)

        self.unit_edit.setText(str(d.get("unit")))

        self.price_spin.setValue(round(float(d.get("price")), 2))

        self.discount_spin.setValue(int(d.get("discount")))

        self.stock_spin.setValue(int(d.get("stock")))

    def load_combos(self):
        types = self.db.get_types()
        for item in types:
            self.type_combo.addItem(item.get('type_name'), item.get('type_id'))

        cats = self.db.get_categories()
        for item in cats:
            self.cat_combo.addItem(item.get('category_name'), item.get('category_id'))

        manuf = self.db.get_manufacturers()
        for item in manuf:
            self.manuf_combo.addItem(item.get('manufacturer_name'), item.get('manufacturer_id'))

        suppliers = self.db.get_suppliers()
        for item in suppliers:
            self.supplier_combo.addItem(item.get('supplier_name'), item.get('supplier_id'))

    def connect_btns(self):
        self.choose_pic_btn.clicked.connect(self.choose_pic)
        self.clear_pic_btn.clicked.connect(self.clear_pic)
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

    def choose_pic(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите картинку товара", "",
                                              "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)")
        if path and os.path.exists(path):
            self.new_img_path = path
            self.img_lbl.setPixmap(_ensure_pixmap(path, QSize(180, 150)))

    def clear_pic(self):
        self.cleared_img = True
        self.new_img_path = None
        self.img_lbl.setPixmap(_ensure_pixmap("", QSize(180, 150)))

    def save(self):
        type_id = self.type_combo.currentData()
        cat_id = self.cat_combo.currentData()
        desc = self.desc_edit.toPlainText().strip()
        manuf_id = self.manuf_combo.currentData()
        supplier_id = self.supplier_combo.currentData()
        unit = self.unit_edit.text().strip()
        price = float(self.price_spin.value())
        discount = int(self.discount_spin.value())
        stock = int(self.stock_spin.value())

        if not all((type_id, cat_id, desc, manuf_id, supplier_id, unit, price)):
            QMessageBox.warning(self, "Ошибка", "Необходимо заполнить все поля отмеченные <*>")
            return

        saved_photo_name = self.old_img_name
        saved_photo = None
        saved_path = None

        if self.cleared_img and self.old_img_name:
            old_img_path = str(os.path.join(IMAGES_DIR, self.old_img_name))
            Path(old_img_path).unlink(missing_ok=True)
            saved_photo_name = None

        if self.new_img_path:
            new_img_name = os.path.basename(self.new_img_path)
            saved_path = str(os.path.join(IMAGES_DIR, new_img_name))
            saved_photo_name = new_img_name
            saved_photo = QPixmap(self.new_img_path)
            if saved_photo.width() > 300 or saved_photo.height() > 200:
                saved_photo = saved_photo.scaled(QSize(300, 200))
            if self.old_img_name:
                old_img_path = str(os.path.join(IMAGES_DIR, self.old_img_name))
                Path(old_img_path).unlink(missing_ok=True)

        if self.data:
            product_id = self.data.get("product_id")
            self.db.update_product(product_id, type_id, cat_id, desc, manuf_id, supplier_id, unit, price, discount, stock,
                                   saved_photo_name)
        else:
            self.db.insert_product(type_id, cat_id, desc, manuf_id, supplier_id, unit, price, discount, stock,
                                   saved_photo_name)

        if saved_photo:
            saved_photo.save(saved_path)

        self.accept()
