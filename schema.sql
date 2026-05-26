CREATE DATABASE  IF NOT EXISTS `demo_5` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `demo_5`;

DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
  category_id int NOT NULL AUTO_INCREMENT,
  category_name varchar(128) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (category_id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


LOCK TABLES categories WRITE;
INSERT INTO categories VALUES (1,'Женская обувь'),(2,'Мужская обувь');
UNLOCK TABLES;


DROP TABLE IF EXISTS delivery_adresses;
CREATE TABLE delivery_adresses (
  delivery_id int NOT NULL AUTO_INCREMENT,
  delivery_address varchar(1024) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (delivery_id)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


LOCK TABLES delivery_adresses WRITE;
INSERT INTO delivery_adresses VALUES (1,'420151, г. Лесной, ул. Вишневая, 32'),(2,'125061, г. Лесной, ул. Подгорная, 8'),(3,'630370, г. Лесной, ул. Шоссейная, 24'),(4,'400562, г. Лесной, ул. Зеленая, 32'),(5,'614510, г. Лесной, ул. Маяковского, 47'),(6,'410542, г. Лесной, ул. Светлая, 46'),(7,'620839, г. Лесной, ул. Цветочная, 8'),(8,'443890, г. Лесной, ул. Коммунистическая, 1'),(9,'603379, г. Лесной, ул. Спортивная, 46'),(10,'603721, г. Лесной, ул. Гоголя, 41'),(11,'410172, г. Лесной, ул. Северная, 13'),(12,'614611, г. Лесной, ул. Молодежная, 50'),(13,'454311, г.Лесной, ул. Новая, 19'),(14,'660007, г.Лесной, ул. Октябрьская, 19'),(15,'603036, г. Лесной, ул. Садовая, 4'),(16,'394060, г.Лесной, ул. Фрунзе, 43'),(17,'410661, г. Лесной, ул. Школьная, 50'),(18,'625590, г. Лесной, ул. Коммунистическая, 20'),(19,'625683, г. Лесной, ул. 8 Марта'),(20,'450983, г.Лесной, ул. Комсомольская, 26'),(21,'394782, г. Лесной, ул. Чехова, 3'),(22,'603002, г. Лесной, ул. Дзержинского, 28'),(23,'450558, г. Лесной, ул. Набережная, 30'),(24,'344288, г. Лесной, ул. Чехова, 1'),(25,'614164, г.Лесной,  ул. Степная, 30'),(26,'394242, г. Лесной, ул. Коммунистическая, 43'),(27,'660540, г. Лесной, ул. Солнечная, 25'),(28,'125837, г. Лесной, ул. Шоссейная, 40'),(29,'125703, г. Лесной, ул. Партизанская, 49'),(30,'625283, г. Лесной, ул. Победы, 46'),(31,'614753, г. Лесной, ул. Полевая, 35'),(32,'426030, г. Лесной, ул. Маяковского, 44'),(33,'450375, г. Лесной ул. Клубная, 44'),(34,'625560, г. Лесной, ул. Некрасова, 12'),(35,'630201, г. Лесной, ул. Комсомольская, 17'),(36,'190949, г. Лесной, ул. Мичурина, 26'),(37,'dfdfsfds'),(38,'dddd');
UNLOCK TABLES;



DROP TABLE IF EXISTS manufacturers;
CREATE TABLE manufacturers (
  manufacturer_id int NOT NULL AUTO_INCREMENT,
  manufacturer_name varchar(128) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (manufacturer_id)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


LOCK TABLES manufacturers WRITE;
INSERT INTO manufacturers VALUES (1,'Kari'),(2,'Marco Tozzi'),(3,'Рос'),(4,'Rieker'),(5,'Alessio Nesca'),(6,'CROSBY');
UNLOCK TABLES;


DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
  order_id int NOT NULL,
  product_id int NOT NULL,
  quantity int NOT NULL,
  PRIMARY KEY (order_id,product_id),
  KEY products_idx (product_id),
  CONSTRAINT orders FOREIGN KEY (order_id) REFERENCES orders (order_id),
  CONSTRAINT products FOREIGN KEY (product_id) REFERENCES products (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

LOCK TABLES order_items WRITE;
INSERT INTO order_items VALUES (1,1,2),(1,2,2),(2,3,1),(2,4,1),(3,5,10),(3,6,10),(4,7,5),(4,8,4),(5,1,2),(5,2,2),(6,3,1),(6,4,1),(7,5,10),(7,6,10),(8,7,5),(8,8,4),(9,9,5),(9,10,1),(10,11,5),(10,12,5);
UNLOCK TABLES;


DROP TABLE IF EXISTS order_statuses;
CREATE TABLE order_statuses (
  status_id int NOT NULL AUTO_INCREMENT,
  status_name varchar(128) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (status_id)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


LOCK TABLES order_statuses WRITE;
INSERT INTO order_statuses VALUES (1,'Новый'),(2,'В обработке'),(3,'В доставке'),(4,'Завершен');
UNLOCK TABLES;


DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id int NOT NULL AUTO_INCREMENT,
  order_date date NOT NULL,
  delivery_date date DEFAULT NULL,
  delivery_id int NOT NULL,
  user_id int NOT NULL,
  `code` int DEFAULT NULL,
  status_id int NOT NULL,
  PRIMARY KEY (order_id),
  KEY status_idx (status_id),
  KEY delivery_idx (delivery_id),
  KEY users_idx (user_id),
  CONSTRAINT delivery FOREIGN KEY (delivery_id) REFERENCES delivery_adresses (delivery_id),
  CONSTRAINT `status` FOREIGN KEY (status_id) REFERENCES order_statuses (status_id),
  CONSTRAINT users FOREIGN KEY (user_id) REFERENCES users (user_id)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

LOCK TABLES orders WRITE;
INSERT INTO orders VALUES (1,'2025-02-26','2025-05-11',1,4,901,4),(2,'2022-09-28','2025-04-21',11,1,902,4),(3,'2025-03-21','2025-04-22',2,2,903,4),(4,'2025-02-20','2025-04-23',11,3,904,4),(5,'2025-03-17','2025-04-24',2,4,905,4),(6,'2025-03-01','2025-04-25',15,1,906,4),(7,'2025-02-28','2025-04-26',3,2,907,4),(8,'2025-03-31','2025-04-27',19,3,908,1),(9,'2025-04-02','2025-04-28',5,4,909,1),(10,'2025-04-03','2025-04-29',19,4,910,1),(11,'1999-12-31','2004-02-12',38,1,NULL,1);
UNLOCK TABLES;


DROP TABLE IF EXISTS product_types;
CREATE TABLE product_types (
  type_id int NOT NULL AUTO_INCREMENT,
  type_name varchar(128) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (type_id)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


LOCK TABLES product_types WRITE;
INSERT INTO product_types VALUES (1,'Ботинки'),(2,'Туфли'),(3,'Кроссовки'),(4,'Полуботинки'),(5,'Кеды'),(6,'Тапочки'),(7,'Сапоги');
UNLOCK TABLES;


DROP TABLE IF EXISTS products;
CREATE TABLE products (
  product_id int NOT NULL AUTO_INCREMENT,
  article varchar(10) COLLATE utf8mb4_bin DEFAULT NULL,
  type_id int NOT NULL,
  unit varchar(10) COLLATE utf8mb4_bin NOT NULL,
  price decimal(10,2) NOT NULL,
  supplier_id int NOT NULL,
  manufacturer_id int NOT NULL,
  category_id int NOT NULL,
  discount int DEFAULT '0',
  stock int DEFAULT '0',
  `description` varchar(1024) COLLATE utf8mb4_bin NOT NULL,
  photo varchar(1024) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (product_id),
  KEY types_idx (type_id),
  KEY suppliers_idx (supplier_id),
  KEY cats_idx (category_id),
  KEY manufacturer_idx (manufacturer_id),
  CONSTRAINT cats FOREIGN KEY (category_id) REFERENCES categories (category_id),
  CONSTRAINT manufacturer FOREIGN KEY (manufacturer_id) REFERENCES manufacturers (manufacturer_id),
  CONSTRAINT suppliers FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id),
  CONSTRAINT `types` FOREIGN KEY (type_id) REFERENCES product_types (type_id)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


LOCK TABLES products WRITE;
INSERT INTO products VALUES (1,'А112Т4',1,'шт.',4990.00,1,1,1,3,6,'Женские Ботинки демисезонные 1','1.jpg'),(2,'F635R4',1,'шт.',3244.00,2,2,1,2,13,'Ботинки 2 женские демисезонные, размер 39, цвет бежевый','2.jpg'),(3,'H782T5',2,'шт.',4499.00,1,1,2,4,5,'Туфли 1 мужские классика MYZ21AW-450A, размер 43, цвет: черный','3.jpg'),(4,'G783F5',1,'шт.',5900.00,1,3,2,2,8,'Мужские ботинки 3-Обувь кожаные с натуральным мехом','4.jpg'),(5,'J384T6',1,'шт.',3800.00,2,4,2,2,16,'B3430/14 Полуботинки мужские 4','5.jpg'),(6,'D572U8',3,'шт.',4100.00,2,3,2,3,6,'129615-4 Кроссовки мужские','6.jpg'),(7,'F572H7',2,'шт.',2700.00,1,2,1,2,14,'Туфли 2 женские летние, размер 39, цвет черный','7.jpg'),(8,'D329H3',4,'шт.',1890.00,2,5,1,4,4,'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый','8.jpg'),(9,'B320R5',2,'шт.',4300.00,1,4,1,2,6,'Туфли 4 женские демисезонные, размер 41, цвет коричневый','9.jpg'),(10,'G432E4',2,'шт.',2800.00,1,1,1,3,15,'Туфли 1 женские TR-YR-413017, размер 37, цвет: черный','10.jpg'),(11,'S213E3',4,'шт.',2156.00,2,6,2,3,6,'407700/01-01 Полуботинки мужские CROSBY',''),(12,'E482R4',4,'шт.',1800.00,1,1,1,2,14,'Полуботинки 1 женские MYZ20S-149, размер 41, цвет: черный',''),(13,'S634B5',5,'шт.',5500.00,2,6,2,3,0,'Кеды Caprice мужские демисезонные, размер 42, цвет черный',''),(14,'K345R4',4,'шт.',2100.00,2,6,2,2,3,'407700/01-02 Полуботинки мужские CROSBY',''),(15,'O754F4',2,'шт.',5400.00,2,4,1,4,18,'Туфли женские демисезонные 4 артикул 55073-68/37',''),(16,'G531F4',1,'шт.',6600.00,1,1,1,12,9,'Ботинки женские зимние ROMER арт. 893167-01 Черный',''),(17,'J542F5',6,'шт.',500.00,1,1,2,13,0,'6 мужские Арт.70701-55-67син р.41',''),(18,'B431R5',1,'шт.',2700.00,2,4,2,2,5,'Мужские кожаные ботинки/мужские ботинки',''),(19,'P764G4',2,'шт.',6800.00,1,6,1,15,15,'Туфли женские, ARGO, размер 38',''),(20,'C436G5',1,'шт.',10200.00,1,5,1,15,9,'Ботинки женские, ARGO, размер 40',''),(21,'F427R5',1,'шт.',11800.00,2,4,1,15,11,'Ботинки на молнии с декоративной пряжкой FRAU',''),(22,'N457T5',4,'шт.',4600.00,1,6,1,3,13,'Полуботинки Ботинки черные зимние, мех',''),(23,'D364R4',2,'шт.',12400.00,1,1,1,16,5,'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши',''),(24,'S326R5',6,'шт.',9900.00,2,6,2,17,15,'Мужские кожаные 6 \"Профиль С.Дали\"\" \"',''),(25,'L754R4',4,'шт.',1700.00,1,1,1,2,7,'Полуботинки 1 женские WB2020SS-26, размер 38, цвет: черный',''),(26,'M542T5',3,'шт.',2800.00,2,4,2,18,3,'Кроссовки мужские TOFA',NULL),(27,'D268G5',2,'шт.',4399.00,2,4,1,3,12,'Туфли 4 женские демисезонные, размер 36, цвет коричневый','план.jpg'),(28,'T324F5',7,'шт.',4699.00,1,6,1,2,5,'Сапоги замша Цвет: синий',''),(29,'K358H6',6,'шт.',599.00,1,4,2,20,2,'6 мужские син р.41',''),(30,'H535R5',1,'шт.',2300.00,2,4,1,2,7,'Женские Ботинки демисезонные',''),(31,NULL,2,'комбо.',267.00,1,1,1,5,1,'ням ням',NULL);
UNLOCK TABLES;


DROP TABLE IF EXISTS roles;
CREATE TABLE roles (
  role_id int NOT NULL AUTO_INCREMENT,
  role_name varchar(128) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (role_id)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES roles WRITE;
INSERT INTO roles VALUES (1,'Администратор'),(2,'Менеджер'),(3,'Авторизированный клиент');
UNLOCK TABLES;


DROP TABLE IF EXISTS suppliers;
CREATE TABLE suppliers (
  supplier_id int NOT NULL AUTO_INCREMENT,
  supplier_name varchar(128) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (supplier_id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;



LOCK TABLES suppliers WRITE;
INSERT INTO suppliers VALUES (1,'Kari'),(2,'Обувь для вас');
UNLOCK TABLES;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  user_id int NOT NULL AUTO_INCREMENT,
  user_name varchar(256) COLLATE utf8mb4_bin NOT NULL,
  user_login varchar(128) COLLATE utf8mb4_bin NOT NULL,
  user_pass varchar(128) COLLATE utf8mb4_bin NOT NULL,
  role_id int NOT NULL,
  PRIMARY KEY (user_id),
  KEY role_idx (role_id),
  CONSTRAINT `role` FOREIGN KEY (role_id) REFERENCES roles (role_id)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


LOCK TABLES users WRITE;
INSERT INTO users VALUES (1,'Никифорова Весения Николаевна','94d5ous@gmail.com','uzWC67',1),(2,'Сазонов Руслан Германович','uth4iz@mail.com','2L6KZG',1),(3,'Одинцов Серафим Артёмович','yzls62@outlook.com','JlFRCZ',1),(4,'Степанов Михаил Артёмович','1diph5e@tutanota.com','8ntwUp',2),(5,'Ворсин Петр Евгеньевич','tjde7c@yahoo.com','YOyhfR',2),(6,'Старикова Елена Павловна','wpmrc3do@tutanota.com','RSbvHv',2),(7,'Михайлюк Анна Вячеславовна','5d4zbu@tutanota.com','rwVDh9',3),(8,'Ситдикова Елена Анатольевна','ptec8ym@yahoo.com','LdNyos',3),(9,'Ворсин Петр Евгеньевич','1qz4kw@mail.com','gynQMT',3),(10,'Старикова Елена Павловна','4np6se@mail.com','AtnDjr',3);
UNLOCK TABLES;
