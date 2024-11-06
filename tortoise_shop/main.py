import asyncio
from tortoise import Tortoise
from config import TORTOISE_ORM  # Импортируем конфигурацию из config.py
from models import Buyer, Medicine, Purchase


async def run():
    # Инициализация Tortoise ORM с использованием конфигурации
    await Tortoise.init(config=TORTOISE_ORM)

    # Генерация схем
    await Tortoise.generate_schemas()

    # Получение всех покупателей
    buyers = await Buyer.all()
    for buyer in buyers:
        print(buyer.name)

    # Закрытие соединений
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(run())

