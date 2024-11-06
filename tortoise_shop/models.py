from tortoise import Model, fields


class Buyer(Model):
    id = fields.IntField(pk=True)  # Первичный ключ
    name = fields.CharField(max_length=100)
    balance = fields.DecimalField(max_digits=10, decimal_places=2)
    age = fields.IntField()

    # связываем Buyer с Purchase
    purchases: fields.ReverseRelation["Purchase"]

    class Meta:
        table = "tortoise_buyer"  # Указываем имя таблицы в БД

    def __str__(self):
        return self.name


class Medicine(Model):
    id = fields.IntField(pk=True)  # Первичный ключ
    title = fields.CharField(max_length=200)
    category = fields.CharField(max_length=100)
    cost = fields.DecimalField(max_digits=10, decimal_places=2)
    description = fields.TextField()
    age_limited = fields.BooleanField(default=False)

    # связываем Medicine с Purchase
    purchases: fields.ReverseRelation["Purchase"]

    class Meta:
        table = "tortoise_medicine"  # Указываем имя таблицы в БД

    def __str__(self):
        return self.title


class Purchase(Model):
    id = fields.IntField(pk=True)  # Первичный ключ
    buyer = fields.ForeignKeyField(
        "models.Buyer",
        related_name="purchases",
        on_delete=fields.CASCADE  # Каскадное удаление
    )
    medicine = fields.ForeignKeyField(
        "models.Medicine",
        related_name="purchases",
        on_delete=fields.CASCADE  # Каскадное удаление
    )
    date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "tortoise_purchase"  # Указываем имя таблицы в БД

    def __str__(self):
        return f"Purchase {self.id}"
