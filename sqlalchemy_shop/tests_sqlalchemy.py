import time
import random
from unittest import TestCase
from .db import SessionLocal, engine
from datetime import datetime
from .models import Buyer, Medicine, Purchase


def write_execution_time(framework, execution_time):
    with open('execution_times.txt', 'a') as f:
        f.write(f"{framework}: {execution_time}\n")


class SQLAlchemyShopTests(TestCase):
    def setUp(self):
        self.session = SessionLocal()
        # Очистка данных перед каждым тестом
        self.session.query(Purchase).delete()
        self.session.query(Medicine).delete()
        self.session.query(Buyer).delete()
        self.session.commit()

    def tearDown(self):
        # Закрываем соединения после завершения тестов
        self.session.close()
        # Очистка данных после каждого теста
        # self.session.query(Purchase).delete()
        # self.session.query(Medicine).delete()
        # self.session.query(Buyer).delete()
        # self.session.commit()

    def test_sqlalchemy(self):
        start_time = time.time()
        #session = SessionLocal()

        # CREATE
        buyers = []
        medicines = []
        for _ in range(1000):
            buyer = Buyer(name='Иван Иванов', balance=1234, age=33)
            medicine = Medicine(title='Лекарство', category='Еда', cost=120.99, description='Описание лекарства')
            self.session.add(buyer)
            self.session.add(medicine)
            buyers.append(buyer)
            medicines.append(medicine)
        self.session.commit()

        for buyer, medicine in zip(buyers, medicines):
            purchase = Purchase(buyer=buyer, medicine=medicine, date=datetime.now())
            self.session.add(purchase)
        self.session.commit()

        self.assertEqual(self.session.query(Buyer).count(), 1000)
        self.assertEqual(self.session.query(Medicine).count(), 1000)
        self.assertEqual(self.session.query(Purchase).count(), 1000)
        print(f"Количество покупателей SQLAlchemy: {self.session.query(Buyer).count()}")
        print(f"Количество лекарств SQLAlchemy: {self.session.query(Medicine).count()}")
        print(f"Количество покупок SQLAlchemy: {self.session.query(Purchase).count()}")

        # READ
        buyers = self.session.query(Buyer).all()
        medicines = self.session.query(Medicine).all()
        purchases = self.session.query(Purchase).all()

        # UPDATE
        for buyer in buyers:
            buyer.balance = 2000
        self.session.commit()

        # DELETE
        self.session.query(Purchase).delete()
        self.session.query(Medicine).delete()
        self.session.query(Buyer).delete()
        self.session.commit()

        end_time = time.time()
        execution_time = end_time - start_time
        write_execution_time('sqlalchemy', execution_time)
        print(f"Время выполнения SQLAlchemy: {execution_time}")
        return execution_time

    def test_sqlalchemy_advanced(self):
        start_time = time.time()

        # CREATE
        buyers = []
        medicines = []
        categories = ['Гомеопатия', 'Болеутоляющие', 'Фитопрепараты', 'Жаропонижающее']
        for i in range(1000):
            buyer = Buyer(
                name=f'Иван Иванов {i + 1}',
                balance=random.uniform(500.01, 2000.01),
                age=random.randint(15, 90)
            )
            medicine = Medicine(
                title=f'Лекарство {i + 1}',
                category=random.choice(categories),
                cost=random.uniform(99.99, 5999.99),
                description='Описание лекарства'
            )
            self.session.add(buyer)
            self.session.add(medicine)
            buyers.append(buyer)
            medicines.append(medicine)
        self.session.commit()

        for buyer, medicine in zip(buyers, medicines):
            purchase = Purchase(buyer=buyer, medicine=medicine, date=datetime.now())
            self.session.add(purchase)
        self.session.commit()

        self.assertEqual(self.session.query(Buyer).count(), 1000)
        self.assertEqual(self.session.query(Medicine).count(), 1000)
        self.assertEqual(self.session.query(Purchase).count(), 1000)

        # СОРТИРОВКА: сортировка покупателей по возрасту
        sorted_buyers = self.session.query(Buyer).order_by(Buyer.age).all()
        print(f"Первый покупатель по возрасту: {sorted_buyers[0].age}")

        # ФИЛЬТРАЦИЯ: найти всех покупателей с балансом больше 1500
        filtered_buyers = self.session.query(Buyer).filter(Buyer.balance > 1500).all()
        print(f"Количество покупателей с балансом больше 1500: {len(filtered_buyers)}")

        # ГРУППИРОВКА: группировка лекарств по категории и подсчет количества в каждой группе
        from sqlalchemy import func
        grouped_medicine = self.session.query(Medicine.category, func.count(Medicine.id)).group_by(
            Medicine.category).all()
        for category, count in grouped_medicine:
            print(f"Категория: {category}, Количество: {count}")

        end_time = time.time()
        execution_time = end_time - start_time
        write_execution_time('sqlalchemy_advanced', execution_time)
        print(f"Время выполнения SQLAlchemy (усложненные операции): {execution_time}")
        return execution_time
