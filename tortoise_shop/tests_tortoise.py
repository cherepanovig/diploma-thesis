import time
import random
from unittest import IsolatedAsyncioTestCase
import time
from unittest import IsolatedAsyncioTestCase
from tortoise import Tortoise
from tortoise.functions import Count
#from config import TORTOISE_ORM
from .models import Buyer, Medicine, Purchase


def write_execution_time(framework, execution_time):
    with open('execution_times.txt', 'a') as f:
        f.write(f"{framework}: {execution_time}\n")


class TortoiseShopTests(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await Tortoise.init(
            db_url="postgres://postgres:Zaq12wsX@localhost:5432/ShopPG",
            modules={'models': ['tortoise_shop.models']}
        )
        await Tortoise.generate_schemas()
        # Очищаем таблицы от предыдущих записей
        await Purchase.all().delete()
        await Medicine.all().delete()
        await Buyer.all().delete()

    # async def asyncSetUp(self):
    #     # Инициализируем Tortoise ORM с нашей конфигурацией
    #     await Tortoise.init(config=TORTOISE_ORM)
    #     # Генерируем схемы в базе данных
    #     await Tortoise.generate_schemas()

    async def asyncTearDown(self):
        # Закрываем соединения после завершения тестов
        await Tortoise.close_connections()

    async def test_tortoise(self):
        start_time = time.time()

        # CREATE
        # for _ in range(1000):
        #     buyer = await Buyer.create(name='Иван Иванов', balance=1234, age=33)
        # for _ in range(1000):
        #     medicine = await Medicine.create(title='Лекарство', category='Еда', cost=120.99,
        #                                      description='Описание лекарства')
        # for _ in range(1000):
        #     purchase = await Purchase.create(buyer=buyer, medicine=medicine)

        buyers = [Buyer(name='Иван Иванов', balance=1234, age=33) for _ in range(1000)]
        await Buyer.bulk_create(buyers)  # метод bulk_create массово создает и сохраняет  объекты в базе данных
        buyers = await Buyer.all()  # Получаем все сохраненные объекты Buyer

        medicines = [Medicine(title='Лекарство', category='Еда', cost=120.99, description='Описание лекарства') for _ in
                     range(1000)]
        await Medicine.bulk_create(medicines)
        medicines = await Medicine.all()  # Получаем все сохраненные объекты Medicine

        purchases = [Purchase(buyer=buyers[i], medicine=medicines[i]) for i in range(1000)]
        await Purchase.bulk_create(purchases)

        # Проверки количества записей:
        self.assertEqual(await Buyer.all().count(), 1000)
        self.assertEqual(await Medicine.all().count(), 1000)
        self.assertEqual(await Purchase.all().count(), 1000)

        print(f"Количество покупателей Tortoise: {await Buyer.all().count()}")
        print(f"Количество лекарств Tortoise: {await Medicine.all().count()}")
        print(f"Количество покупок Tortoise: {await Purchase.all().count()}")

        # READ
        buyers = await Buyer.all()
        medicines = await Medicine.all()
        purchases = await Purchase.all()

        # UPDATE
        buyers = await Buyer.all()
        for buyer in buyers:
            buyer.balance = 2000
            await buyer.save()
            #await Buyer.bulk_update(buyers, fields=['balance'])


        # DELETE
        buyers = await Buyer.all()
        await Purchase.all().delete()
        await Medicine.all().delete()
        await Buyer.all().delete()

        end_time = time.time()
        execution_time = end_time - start_time
        write_execution_time('tortoise', execution_time)
        print(f"Время выполнения Tortoise: {execution_time}")
        # return end_time - start_time

    async def test_tortoise_advanced(self):
        start_time = time.time()
        categories = ['Гомеопатия', 'Болеутоляющие', 'Фитопрепараты', 'Жаропонижающее']

        # CREATE
        buyers = [
            Buyer(
                name=f'Иван Иванов {i + 1}',
                balance=random.uniform(500.01, 2000.01),
                age=random.randint(15, 90)
            ) for i in range(1000)
        ]
        await Buyer.bulk_create(buyers)  # метод bulk_create массово создает и сохраняет  объекты в базе данных
        buyers = await Buyer.all()  # Получаем все сохраненные объекты Buyer

        medicines = [
            Medicine(
                title=f'Лекарство {i + 1}',
                category=random.choice(categories),
                cost=random.uniform(99.99, 5999.99),
                description='Описание лекарства'
            ) for i in range(1000)
        ]
        await Medicine.bulk_create(medicines)
        medicines = await Medicine.all()  # Получаем все сохраненные объекты Medicine

        purchases = [Purchase(buyer=buyers[i], medicine=medicines[i]) for i in range(1000)]
        await Purchase.bulk_create(purchases)

        # Проверки количества записей:
        self.assertEqual(await Buyer.all().count(), 1000)
        self.assertEqual(await Medicine.all().count(), 1000)
        self.assertEqual(await Purchase.all().count(), 1000)

        # СОРТИРОВКА: сортировка покупателей по возрасту
        sorted_buyers = await Buyer.all().order_by('age')
        print(f"Первый покупатель по возрасту: {sorted_buyers[0].age}")

        # ФИЛЬТРАЦИЯ: найти всех покупателей с балансом больше 1500
        filtered_buyers = await Buyer.filter(balance__gt=1500)
        print(f"Количество покупателей с балансом больше 1500: {len(filtered_buyers)}")

        # ГРУППИРОВКА: группировка лекарств по категории и подсчет количества в каждой группе
        grouped_medicine = await Medicine.all().group_by('category').annotate(count=Count('id')).values('category',
                                                                                                        'count')
        for group in grouped_medicine:
            print(f"Категория: {group['category']}, Количество: {group['count']}")

        end_time = time.time()
        execution_time = end_time - start_time
        write_execution_time('tortoise_advanced', execution_time)
        print(f"Время выполнения Tortoise (усложненные операции): {execution_time}")
        return execution_time


# Запуск тестов
if __name__ == "__main__":
    import unittest

    unittest.main()


