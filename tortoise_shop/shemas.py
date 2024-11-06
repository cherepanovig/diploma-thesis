from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional


# Схема для создания покупателя
class CreateBuyer(BaseModel):
    name: str
    balance: Decimal
    age: int


# Схема для обновления покупателя
class UpdateBuyer(BaseModel):
    name: str
    balance: Decimal
    age: int


# Схема для создания лекарства
class CreateMedicine(BaseModel):
    title: str
    category: str
    cost: Decimal
    description: str
    age_limited: bool = False


# Схема для обновления лекарства
class UpdateMedicine(BaseModel):
    title: str
    category: str
    cost: Decimal
    description: str
    age_limited: bool = False


# Схема для создания покупки
class CreatePurchase(BaseModel):
    buyer_id: int
    medicine_id: int
    date: datetime


# Схема для обновления покупки
class UpdatePurchase(BaseModel):
    buyer_id: int
    medicine_id: int
    date: datetime
