from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# создаем пользовательский базовый класс, от которого будут наследоваться все наши модели.
class Base(DeclarativeBase):
    pass


engine = create_engine('postgresql://postgres:Zaq12wsX@localhost/ShopPG')  # создания подключения к базе данных
SessionLocal = sessionmaker(bind=engine)  # для создания сессий работы с базой данных

