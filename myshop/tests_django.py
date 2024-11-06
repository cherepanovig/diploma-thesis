from django.test import TestCase
import time
from .models import Buyer, Medicine, Purchase


def write_execution_time(framework, execution_time):
    with open('execution_times.txt', 'a') as f:
        f.write(f"{framework}: {execution_time}\n")


class MyShopTests(TestCase):
    def test_django(self):
        start_time = time.time()

        # CREAT
        for _ in range(1000):
            buyer = Buyer(name='Иван Иванов', balance=1234, age=33)
            buyer.save()
        for _ in range(1000):
            medicine = Medicine(title='Лекарство', category='Еда', cost=120.99, description='Описание лекарства')
            medicine.save()
        for _ in range(1000):
            purchase = Purchase(buyer=buyer, medicine=medicine)
            purchase.save()

        # если объекты не создаются, тест завершится с ошибкой
        self.assertEqual(Buyer.objects.count(), 1000)
        self.assertEqual(Medicine.objects.count(), 1000)
        self.assertEqual(Purchase.objects.count(), 1000)

        print(f"Количество покупателей Django: {Buyer.objects.count()}")
        print(f"Количество лекарств Django: {Medicine.objects.count()}")
        print(f"Количество покупок Django: {Purchase.objects.count()}")

        # READ
        buyers = Buyer.objects.all()
        medicines = Medicine.objects.all()
        purchases = Purchase.objects.all()

        # UPDATE
        for buyer in buyers:
            buyer.balance = 2000
            buyer.save()

        # DELETE
        Buyer.objects.all().delete()
        Medicine.objects.all().delete()
        Purchase.objects.all().delete()

        end_time = time.time()
        execution_time = end_time - start_time
        write_execution_time('django', execution_time)
        print(f"Время выполнения Django: {execution_time}")
        return execution_time



