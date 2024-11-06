import time
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
        # Очистка данных после каждого теста
        self.session.query(Purchase).delete()
        self.session.query(Medicine).delete()
        self.session.query(Buyer).delete()
        self.session.commit()

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
