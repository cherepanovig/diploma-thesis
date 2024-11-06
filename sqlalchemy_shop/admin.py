# Чтобы избежать зацикленности импортов, вынесем функцию get_db в отдельный модуль.
# Тогда у нас не будет зацикленности импортов между модулями db и models.

from sqlalchemy.orm import sessionmaker
from PG_Django.sqlalchemy_shop.db import SessionLocal, engine

# функция-генератор для подключения к БД
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
