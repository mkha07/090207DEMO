# Демо экзамен профильного уровня

```
DEMO/
├─── docs/ # Диаграмма ER, блок-схема алгоритма
├─── images/ Папка для картинок товаров
├─── resources/ Папка для лого и картинок глушилок
├─── ui/ Файлы Qt Designer
├─── ui_py/ Файлы Qt Designer переведенные в Python через Pyuic6
├─── widgets/ Классы виджетов проекта
├─── windows/ Классы основных окон проекта
├─── dist/ Файл exe
├─── .env.example Пример заполнения .env
├─── requirements.txt Требуемые пакеты
├─── schema.sql Скрипт для БД MySQL
├─── database.py Модуль работы с БД
├─── main.py Точка входа программы
└─── utility.py Вспомогоательные функции
```

## 1. Необходимо скачать пакеты
```bash
pip install -r requirements.txt
```
## 2. Заполнить данные DB_CONFIG .env по примеру .env.example

## 3. Запустить скрипт schema.sql

## 4. Запустить main.py или dist/main.exe

## 5. Отрывок данных для входа (для всех см. БД)
| Логин                | Пароль | Роль                  |
|----------------------|--------|-----------------------|
| 94d5ous@gmail.com    | uzWC67 | Администратор         |
| 1diph5e@tutanota.com | 8ntwUp | Менеджер              |
| ptec8ym@yahoo.com    | LdNyos | Авторизованный клиент |

