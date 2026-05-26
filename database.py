import os

import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv(".env")

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_NAME = os.environ.get("DB_NAME", "demo_5")

DB_CONFIG = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
    "database": DB_NAME
}


class Database:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG, cursorclass=DictCursor)

    def _q(self, sql, args=None):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, args)
            rows = cursor.fetchall()

        return rows

    def _exeq(self, sql, args=None):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, args)
            rid = cursor.lastrowid
        self.conn.commit()
        return rid

    def authenticate(self, login, password):
        user_data = self._q("SELECT u.user_id, u.user_name, r.role_name "
                            "FROM users u JOIN roles r ON u.role_id = r.role_id WHERE user_login = %s"
                            " AND user_pass = %s", (login, password))
        return user_data

    def get_suppliers(self):
        return self._q("SELECT * FROM suppliers")

    def get_types(self):
        return self._q("SELECT * FROM product_types")

    def get_categories(self):
        return self._q("SELECT * FROM categories")

    def get_manufacturers(self):
        return self._q("SELECT * FROM manufacturers")

    def get_products(self, srch=None, supplier_id=None, sort_by="type_name", sort_order="asc"):
        sql = """SELECT product_id, 
                    article, 
                    type_name, 
                    products.type_id,
                    unit, 
                    price, 
                    supplier_name,
                    products.supplier_id, 
                    manufacturer_name, 
                    products.manufacturer_id,
                    category_name, 
                    products.category_id,
                    discount, 
                    stock, 
                    description, 
                    photo
                    FROM products 
                    JOIN product_types ON products.type_id = product_types.type_id
                    JOIN manufacturers ON products.manufacturer_id = manufacturers.manufacturer_id
                    JOIN suppliers ON products.supplier_id = suppliers.supplier_id
                    JOIN categories ON products.category_id = categories.category_id 
                    WHERE 1=1 """
        args = []
        if srch:
            sql += (" AND (type_name LIKE %s OR supplier_name LIKE %s OR manufacturer_name LIKE %s"
                    " OR category_name LIKE %s OR description LIKE %s) ")
            srch_text = srch.strip()
            args.extend([f"%{srch_text}%", f"%{srch_text}%", f"%{srch_text}%", f"%{srch_text}%", f"%{srch_text}%"])

        if supplier_id:
            sql += " AND products.supplier_id = %s "
            args.append(supplier_id)

        sql += f" ORDER BY {sort_by} {sort_order}"

        return self._q(sql, args)

    def insert_product(self, type_id, category_id, description, manuf_id, supplier_id, unit, price, discount, stock,
                       photo=None):
        sql = """INSERT INTO products 
                (`type_id`,
                `unit`,
                `price`,
                `supplier_id`,
                `manufacturer_id`,
                `category_id`,
                `discount`,
                `stock`,
                `description`,
                `photo`) VALUES 
                (%s,
                 %s,
                 %s,
                 %s,
                 %s,
                 %s,
                 %s,
                 %s,
                 %s,
                 %s);"""
        args = (type_id, unit, price, supplier_id, manuf_id, category_id, discount, stock, description, photo)
        return self._exeq(sql, args)

    def update_product(self, product_id, type_id, category_id, description, manuf_id, supplier_id, unit, price,
                       discount, stock,
                       photo=None):
        sql = """
            UPDATE `products`
            SET
            `type_id` = %s,
            `unit` = %s,
            `price` = %s,
            `supplier_id` = %s,
            `manufacturer_id` = %s,
            `category_id` = %s,
            `discount` = %s,
            `stock` = %s,
            `description` = %s,
            `photo` = %s
            WHERE `product_id` = %s;
        """
        args = (type_id, unit, price, supplier_id, manuf_id, category_id, discount, stock, description, photo,
                product_id)

        return self._exeq(sql, args)

    def is_product_in_order(self, product_id):
        rows = self._q("SELECT count(*) as cnt FROM order_items where product_id = %s", product_id)
        count = rows[0].get('cnt', 0)
        return count > 0

    def del_product(self, product_id):
        return self._exeq("DELETE FROM products WHERE product_id = %s", product_id)

    def get_orders(self):
        return self._q("""SELECT o.*, s.status_name, d.delivery_address FROM
                            orders o 
                            JOIN order_statuses s ON o.status_id = s.status_id
                            JOIN delivery_adresses d ON o.delivery_id = d.delivery_id;""")

    def get_clients(self):
        return self._q('SELECT u.user_id, u.user_name, r.role_name '
                       'FROM users u JOIN roles r ON u.role_id = r.role_id')

    def get_statuses(self):
        return self._q("SELECT * FROM order_statuses")

    def insert_new_address(self, delivery_address):
        delivery_id = None
        rows = self._q("SELECT * FROM delivery_adresses WHERE lower(delivery_address) = %s",
                       str(delivery_address).lower())
        if rows:
            delivery_id = rows[0].get("delivery_id")

        return delivery_id if delivery_id else self._exeq(
            "INSERT INTO delivery_adresses (delivery_address) VALUES (%s)",
            delivery_address)

    def insert_order(self, status_id, user_id, delivery_address, order_date, delivery_date):
        delivery_id = self.insert_new_address(delivery_address)

        return self._exeq("""
                INSERT INTO orders
                        (`order_date`,
                        `delivery_date`,
                        `delivery_id`,
                        `user_id`,
                        `status_id`)
                        VALUES
                        (%s,
                        %s,
                        %s,
                        %s,
                        %s);
        """, (order_date, delivery_date, delivery_id, user_id, status_id))

    def update_order(self, order_id, status_id, user_id, delivery_address, order_date, delivery_date):
        delivery_id = self.insert_new_address(delivery_address)
        return self._exeq("""
                UPDATE `orders`
                SET
                `order_date` = %s,
                `delivery_date` = %s,
                `delivery_id` = %s,
                `user_id` = %s,
                `status_id` = %s
                WHERE `order_id` = %s;
        """, (order_date, delivery_date, delivery_id, user_id, status_id, order_id))

    def del_order(self, order_id):
        return self._exeq("DELETE FROM orders WHERE order_id = %s", order_id)
