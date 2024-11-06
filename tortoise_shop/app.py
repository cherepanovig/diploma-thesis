from fastapi import FastAPI, HTTPException, APIRouter, status
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from typing import List
from models import Buyer, Medicine, Purchase
from shemas import (
    CreateBuyer, UpdateBuyer,
    CreateMedicine, UpdateMedicine,
    CreatePurchase, UpdatePurchase
)
from config import TORTOISE_ORM

app = FastAPI(title="Аптека API",
              description="API Tortoise для управления аптекой",
              version="1.0.0")

# Создаем роутер с префиксом '/buyer' и тегом 'Покупатели'
router_b = APIRouter(prefix='/buyer', tags=['Покупатели'])

# Создаем роутер с префиксом '/medicine' и тегом 'Лекарства'
router_m = APIRouter(prefix='/medicine', tags=['Лекарства'])


# Корневой путь
@app.get("/")
async def root():
    return {"message": "Welcome to Pharmacy API"}


# Регистрируем эндпоинты для покупателей

# Маршрут для создания нового покупателя
@router_b.post('/create')
async def create_buyer(buyer: CreateBuyer):
    new_buyer = await Buyer.create(**buyer.model_dump())
    return new_buyer


# Маршрут для получения всех покупателей
@router_b.get('/')
async def get_buyers():
    buyers = await Buyer.all()
    if not buyers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no buyers'
        )
    return buyers


# Маршрут для получения покупателя по ID
@router_b.get('/{buyer_id}')
async def get_buyer(buyer_id: int):
    buyer = await Buyer.get_or_none(id=buyer_id)
    if buyer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer was not found"
        )
    return buyer


# Маршрут для  обновления покупателя
@router_b.put('/update/{buyer_id}')
async def update_buyer(buyer_id: int, buyer: UpdateBuyer):
    buyer_upd = await Buyer.get_or_none(id=buyer_id)
    if buyer_upd is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer was not found"
        )
    # заменяем поля
    buyer_upd.name = buyer.name
    buyer_upd.balance = buyer.balance
    buyer_upd.age = buyer.age
    await buyer_upd.save()
    return buyer_upd


# Маршрут для удаления покупателя вместе с его покупками
@router_b.delete('/delete/{buyer_id}')
async def delete_buyer(buyer_id: int):
    buyer = await Buyer.get_or_none(id=buyer_id)
    if buyer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer was not found"
        )

    await buyer.delete()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Buyer and all related purchases were successfully deleted!'
    }


# Маршрут для получения всех Medicine конкретного Buyer по id
@router_b.get('/{buyer_id}/medicines')
async def get_buyer_medicines(buyer_id: int):
    # Проверяем существование покупателя
    buyer = await Buyer.get_or_none(id=buyer_id)
    if buyer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer was not found"
        )
    # Получаем все лекарства, которые купил данный покупатель без дублей
    medicines = await Medicine.filter(purchases__buyer=buyer).distinct()

    if not medicines:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This buyer hasn't purchased any medicines yet"
        )

    return medicines


# Подключаем роутер для покупателей
app.include_router(router_b)


# Регистрируем эндпоинты для лекарств

# Маршрут для создания нового лекарства
@router_m.post('/create')
async def create_medicine(medicine: CreateMedicine):
    new_medicine = await Medicine.create(**medicine.model_dump())
    return new_medicine


# Маршрут для получения всех лекарств
@router_m.get('/')
async def get_medicines():
    medicines = await Medicine.all()
    if not medicines:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no medicines'
        )
    return medicines


# Маршрут для получения лекарства по ID
@router_m.get('/{medicine_id}')
async def get_medicine(medicine_id: int):
    medicine = await Medicine.get_or_none(id=medicine_id)
    if medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine was not found"
        )
    return medicine


# Маршрут для  обновления лекарства
@router_m.put('/update/{medicine_id}')
async def update_medicine(medicine_id: int, medicine: UpdateMedicine):
    medicine_upd = await Medicine.get_or_none(id=medicine_id)
    if medicine_upd is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine was not found"
        )
    # заменяем поля
    medicine_upd.title = medicine.title
    medicine_upd.category = medicine.category
    medicine_upd.cost = medicine.cost
    medicine_upd.description = medicine.description
    medicine_upd.age_limited = medicine.age_limited
    await medicine_upd.save()
    return medicine_upd


# Маршрут для удаления лекарства
@router_m.delete('/delete/{medicine_id}')
async def delete_medicine(medicine_id: int):
    medicine = await Medicine.get_or_none(id=medicine_id)
    if medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine was not found"
        )

    await medicine.delete()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Medicine and all related purchases were successfully deleted!'
    }


# Подключаем роутер для лекарств
app.include_router(router_m)

# Создаем маршруты для Purchase

# Создаем роутер с префиксом '/purchase' и тегом 'Покупки'
router_p = APIRouter(prefix='/purchase', tags=['Покупки'])


# Регистрируем эндпоинты для покупок

# Маршрут для получения всех покупок
@router_p.get('/')
async def get_purchases():
    purchases = await Purchase.all()
    if not purchases:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no purchases'
        )
    return purchases

# Маршрут для получения покупки по ID
@router_p.get('/{purchase_id}')
async def get_purchase(purchase_id: int):
    purchase = await Purchase.get_or_none(id=purchase_id)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Purchase not found'
        )
    return purchase

# Маршрут для создания новой покупки
@router_p.post('/')
async def create_purchase(purchase: CreatePurchase):
    buyer = await Buyer.get_or_none(id=purchase.buyer_id)
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Buyer not found'
        )
    medicine = await Medicine.get_or_none(id=purchase.medicine_id)
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Medicine not found'
        )
    purchase_new = await Purchase.create(
        buyer=buyer,
        medicine=medicine,
        date=purchase.date
    )
    return purchase_new

# Маршрут для обновления покупки
@router_p.put('/{purchase_id}')
async def update_purchase(purchase_id: int, purchase_upd: UpdatePurchase):
    purchase = await Purchase.get_or_none(id=purchase_id)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Purchase not found'
        )
    # Обновляем покупателя
    buyer = await Buyer.get_or_none(id=purchase_upd.buyer_id)
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Buyer not found'
        )
    purchase.buyer = buyer
    # Обновляем лекарство
    medicine = await Medicine.get_or_none(id=purchase_upd.medicine_id)
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Medicine not found'
        )
    purchase.medicine = medicine
    # Обновляем дату
    purchase.date = purchase_upd.date
    await purchase.save()
    return purchase

# Маршрут для удаления покупки
@router_p.delete('/{purchase_id}')
async def delete_purchase(purchase_id: int):
    purchase = await Purchase.get_or_none(id=purchase_id)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Purchase not found'
        )
    await purchase.delete()
    return {
        'status_code': status.HTTP_200_OK,
        'detail': 'Purchase deleted successfully'
    }


# Подключаем роутер для покупок
app.include_router(router_p)

# Регистрируем Tortoise
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
