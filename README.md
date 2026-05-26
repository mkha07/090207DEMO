# Демо экзамен профильного уровня

## Структура проекта

```
DEMO05/
├── main.py  # Точка входа: QApplication + стили + запуск LoginWindow
├── database.py # Класс Database: всё взаимодействие с MySQL
├── utility.py  # Константы путей, роли, вспомогательная ensure_pixmap()
├── schema.sql  # SQL-скрипт создания и наполнения БД
│
├── windows/ # Главные окна приложения
│   ├── Login.py # LoginWindow — окно входа (логин/пароль или гость)
│   └── Main.py # MainWindow — основное окно (товары / заказы)
│
├── widgets/ # Переиспользуемые виджеты
│   ├── ProductFrame.py # Карточка товара (отображение + выбор + двойной клик)
│   ├── OrderFrame.py   # Карточка заказа
│   ├── ProductDialog.py # Диалог добавления/редактирования товара
│   └── OrderDialog.py  # Диалог добавления/редактирования заказа
│
├── ui_py/   # Сгенерированные pyuic6 классы из Qt Designer (.ui)
├── ui/      # Исходные файлы Qt Designer (.ui)
├── images/  # Фото товаров
├── resources/  # Иконка, заглушка-картинка
├── docs/    # ER-диаграмма, блок-схемы
└── dist/    # Готовый .exe
```

## Быстрый старт

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Заполнить .env (по образцу .env.example)

# 3. Создать БД
mysql -u root -p < schema.sql

# 4. Запустить
python main.py
```

## Тестовые логины

| Логин                | Пароль | Роль                   |
|----------------------|--------|------------------------|
| 94d5ous@gmail.com    | uzWC67 | Администратор          |
| 1diph5e@tutanota.com | 8ntwUp | Менеджер               |
| ptec8ym@yahoo.com    | LdNyos | Авторизованный клиент  |
