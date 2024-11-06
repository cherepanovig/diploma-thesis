import psycopg2
from psycopg2 import sql

# Параметры подключения к PostgreSQL
HOST = "localhost"
PORT = "5432"
USER = "postgres"  # имя пользователя
PASSWORD = "Zaq12wsX"  # пароль

# Подключение к серверу PostgreSQL
conn = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PASSWORD)

# Включение автокоммита
conn.autocommit = True

# Создание курсора
cursor = conn.cursor()

# Имя базы данных
db_name = "ShopPG"

# Команда для создания базы данных
create_db_query = sql.SQL("""
    CREATE DATABASE {}
    WITH OWNER = {}
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TEMPLATE = template0;
""").format(sql.Identifier(db_name), sql.Identifier(USER))

try:
    # Выполнение команды создания базы данных
    cursor.execute(create_db_query)
    print(f"База данных '{db_name}' успешно создана.")
except psycopg2.Error as e:
    print(f"Ошибка при создании базы данных: {e}")
finally:
    # Закрытие курсора и соединения
    cursor.close()
    conn.close()
