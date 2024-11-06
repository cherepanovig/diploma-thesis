from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Buyer(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # всего цифр 10 из них 2 после запятой
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]  # добавил ограничение по возрасту
    )

    def __str__(self):
        return self.name


class Medicine(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()  # описание с неограниченным количеством текста
    age_limited = models.BooleanField(default=False)  # ограничение по возрасту 18+ (булево поле по дефолту False)


    def __str__(self):
        return self.title


class Purchase(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
