from django.test import TestCase
import time
import random
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

    def test_django_advanced(self):
        start_time = time.time()

        # CREAT
        for i in range(1000):
            buyer = Buyer(
                name=f'Иван Иванов {i + 1}',  # Добавляем порядковый номер
                balance=random.uniform(500.01, 2000.01),  # Случайный баланс
                age=random.randint(15, 90)  # Случайный возраст
            )
            buyer.save()

        categories = ['Гомеопатия', 'Болеутоляющие', 'Фитопрепараты', 'Жаропонижающее']
        for i in range(1000):
            medicine = Medicine(
                title=f'Лекарство {i + 1}',  # Добавляем порядковый номер
                category=random.choice(categories),  # Случайная категория
                cost=random.uniform(99.99, 5999.99),  # Случайная стоимость
                description='Описание лекарства'
            )
            medicine.save()

        buyers = Buyer.objects.all()
        medicines = Medicine.objects.all()
        for i in range(1000):  # используем созданные объекты
            purchase = Purchase(buyer=buyers[i], medicine=medicines[i])
            purchase.save()

        # если объекты не создаются, тест завершится с ошибкой
        self.assertEqual(Buyer.objects.count(), 1000)
        self.assertEqual(Medicine.objects.count(), 1000)
        self.assertEqual(Purchase.objects.count(), 1000)

        # СОРТИРОВКА: сортировка покупателей по возрасту
        sorted_buyers = Buyer.objects.order_by('age')
        print(f"Первый покупатель по возрасту: {sorted_buyers.first().age}")

        # ФИЛЬТРАЦИЯ: найти всех покупателей с балансом больше 1500
        filtered_buyers = Buyer.objects.filter(balance__gt=1500)
        print(f"Количество покупателей с балансом больше 1500: {filtered_buyers.count()}")

        # ГРУППИРОВКА: группировка лекарств по категории и подсчет количества в каждой группе
        from django.db.models import Count
        grouped_medicine = Medicine.objects.values('category').annotate(count=Count('id'))
        for group in grouped_medicine:
            print(f"Категория: {group['category']}, Количество: {group['count']}")


        end_time = time.time()
        execution_time = end_time - start_time
        write_execution_time('django_advanced', execution_time)
        print(f"Время выполнения Django (усложненные операции): {execution_time}")
        return execution_time


