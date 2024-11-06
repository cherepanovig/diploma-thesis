from PG_Django.sqlalchemy_shop.models import Buyer, Medicine, Purchase  # Импортируем модели
from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from PG_Django.sqlalchemy_shop.admin import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from PG_Django.sqlalchemy_shop.shemas import (CreateBuyer, UpdateBuyer, CreateMedicine, UpdateMedicine,
                                              CreatePurchase, UpdatePurchase)

# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify
from decimal import Decimal
from sqlalchemy import and_

# Создаем роутер с префиксом '/buyer' и тегом 'buyer'
router_b = APIRouter(prefix='/buyer', tags=['buyer'])


# Создаем маршруты для Buyer

# Маршрут для получения всех покупателей
@router_b.get('/')
async def all_buyers(db: Annotated[Session, Depends(get_db)]):
    buyers = db.query(Buyer).all()
    if not buyers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no buyers'
        )
    return buyers


# Маршрут для получения покупателя по ID
@router_b.get('/{buyer_id}')
async def buyer_by_id(buyer_id: int, db: Annotated[Session, Depends(get_db)]):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if buyer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer was not found"
        )
    return buyer


# Маршрут для создания нового покупателя
@router_b.post('/create')
async def create_buyer(buyer: CreateBuyer, db: Annotated[Session, Depends(get_db)]):
    new_buyer = Buyer(
        name=buyer.name,
        balance=buyer.balance,
        age=buyer.age,
        slug=slugify(buyer.name)
    )
    db.add(new_buyer)
    db.commit()
    db.refresh(new_buyer)
    return new_buyer


# Маршрут для обновления покупателя
@router_b.put('/update/{buyer_id}')
async def update_buyer(buyer_id: int, buyer: UpdateBuyer, db: Annotated[Session, Depends(get_db)]):
    upd_buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if upd_buyer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer was not found"
        )

    upd_buyer.name = buyer.name
    upd_buyer.balance = buyer.balance
    upd_buyer.age = buyer.age
    upd_buyer.slug = slugify(buyer.name)

    db.commit()
    db.refresh(upd_buyer)

    return upd_buyer


# # Маршрут для удаления покупателя вместе с его покупками
# @router_b.delete('/delete/{buyer_id}')
# async def delete_buyer(buyer_id: int, db: Annotated[Session, Depends(get_db)]):
#     buyer = db.scalar(select(Buyer).where(Buyer.id == buyer_id))
#     if buyer is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Buyer was not found"
#         )
#
#     # Удаление покупок покупателя
#     db.execute(delete(Purchase).where(Purchase.buyer_id == buyer_id))
#
#     # Удаление покупателя
#     db.execute(delete(Buyer).where(Buyer.id == buyer_id))
#
#     db.commit()
#
#     return {'status_code': status.HTTP_200_OK, 'transaction': 'Buyer and all related purchases were '
#                                                               'successfully deleted!'}

# Маршрут для удаления покупателя вместе с его покупками
@router_b.delete('/delete/{buyer_id}')
async def delete_buyer(buyer_id: int, db: Annotated[Session, Depends(get_db)]):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if buyer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer was not found"
        )

    # Удаление покупателя и связанных покупок
    db.delete(buyer)
    db.commit()

    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Buyer and all related purchases were successfully deleted!'}


# # Маршрут для получения всех Medicine конкретного Buyer по id
# @router_b.get('/{buyer_id}/medicines')
# async def get_buyer_medicines(buyer_id: int, db: Annotated[Session, Depends(get_db)]):
#     # Проверяем существование покупателя
#     buyer = db.scalar(select(Buyer).where(Buyer.id == buyer_id))
#     if buyer is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Buyer was not found"
#         )
#
#     # Получаем все лекарства, которые купил данный покупатель
#     medicines = db.scalars(
#         select(Medicine)
#         .join(Purchase, and_(Purchase.medicine_id == Medicine.id))
#         .where(Purchase.buyer_id == buyer_id)
#     ).all()
#
#     if not medicines:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="This buyer hasn't purchased any medicines yet"
#         )
#
#     return medicines

# Маршрут для получения всех Medicine конкретного Buyer по id
@router_b.get('/{buyer_id}/medicines')
async def get_buyer_medicines(buyer_id: int, db: Annotated[Session, Depends(get_db)]):
    # Проверяем существование покупателя
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if buyer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer was not found"
        )
    # Получаем все лекарства, которые купил данный покупатель
    medicines = db.query(Medicine).join(Purchase).filter(Purchase.buyer_id == buyer_id).all()

    if not medicines:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This buyer hasn't purchased any medicines yet"
        )

    return medicines


# Создаем маршруты для Medicine

# Создаем роутер с префиксом '/medicine' и тегом 'medicine'
router_m = APIRouter(prefix='/medicine', tags=['medicine'])


# Маршрут для получения всех лекарств
@router_m.get('/')
async def all_medicines(db: Annotated[Session, Depends(get_db)]):
    medicines = db.query(Medicine).all()
    if not medicines:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no medicines'
        )
    return medicines


# Маршрут для получения лекарства по ID
@router_m.get('/{medicine_id}')
async def medicine_by_id(medicine_id: int, db: Annotated[Session, Depends(get_db)]):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine was not found"
        )
    return medicine


# Маршрут для создания нового лекарства
@router_m.post('/create')
async def create_medicine(medicine: CreateMedicine, db: Annotated[Session, Depends(get_db)]):
    new_medicine = Medicine(
        title=medicine.title,
        category=medicine.category,
        cost=medicine.cost,
        description=medicine.description,
        slug=slugify(medicine.title)
    )
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)
    return new_medicine


# Маршрут для обновления лекарства
@router_m.put('/update/{medicine_id}')
async def update_medicine(medicine_id: int, medicine: UpdateMedicine, db: Annotated[Session, Depends(get_db)]):
    upd_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if upd_medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine was not found"
        )

    upd_medicine.title = medicine.title
    upd_medicine.category = medicine.category
    upd_medicine.cost = medicine.cost
    upd_medicine.description = medicine.description
    upd_medicine.slug = slugify(medicine.title)

    db.commit()
    db.refresh(upd_medicine)

    return upd_medicine


# Маршрут для удаления лекарства
@router_m.delete('/delete/{medicine_id}')
async def delete_medicine(medicine_id: int, db: Annotated[Session, Depends(get_db)]):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine was not found"
        )

    # Удаление лекарства
    db.delete(medicine)
    db.commit()

    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Medicine and all related purchases were successfully deleted!'}


# Создаем маршруты для Purchase

# Создаем роутер с префиксом '/purchase' и тегом 'purchase'
router_p = APIRouter(prefix='/purchase', tags=['purchase'])


# Маршрут для получения всех покупок
@router_p.get('/')
async def all_purchases(db: Annotated[Session, Depends(get_db)]):
    purchases = db.query(Purchase).all()
    if not purchases:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no purchases'
        )
    return purchases


# Маршрут для получения покупки по ID
@router_p.get('/{purchase_id}')
async def purchase_by_id(purchase_id: int, db: Annotated[Session, Depends(get_db)]):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if purchase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase was not found"
        )
    return purchase


# Маршрут для создания новой покупки
@router_p.post('/create')
async def create_purchase(purchase: CreatePurchase, db: Annotated[Session, Depends(get_db)]):
    # Проверка существования покупателя
    buyer = db.query(Buyer).filter(Buyer.id == purchase.buyer_id).first()
    if buyer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer not found"
        )

    # Проверка существования лекарства
    medicine = db.query(Medicine).filter(Medicine.id == purchase.medicine_id).first()
    if medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )

    # Создание новой покупки
    new_purchase = Purchase(
        buyer_id=purchase.buyer_id,
        medicine_id=purchase.medicine_id,
        date=purchase.date
    )

    # Добавление новой покупки в сессию БД
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    return new_purchase


# Маршрут для обновления покупки
@router_p.put('/update/{purchase_id}')
async def update_purchase(purchase_id: int, purchase: UpdatePurchase, db: Annotated[Session, Depends(get_db)]):
    # Найти покупку по ID
    upd_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()

    # Если покупка не найдена, выбрасываем исключение
    if upd_purchase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found"
        )

    # Проверка, существует ли новый buyer_id в таблице Buyer
    if not db.query(Buyer).filter(Buyer.id == purchase.buyer_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Buyer not found"
        )

    # Проверка, существует ли новый medicine_id в таблице Medicine
    if not db.query(Medicine).filter(Medicine.id == purchase.medicine_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medicine not found"
        )

    # Обновляем атрибуты объекта
    upd_purchase.buyer_id = purchase.buyer_id
    upd_purchase.medicine_id = purchase.medicine_id
    upd_purchase.date = purchase.date

    # Сохраняем изменения в БД
    db.commit()
    db.refresh(upd_purchase)

    return upd_purchase


# Маршрут для удаления покупки
@router_p.delete('/delete/{purchase_id}')
async def delete_purchase(purchase_id: int, db: Annotated[Session, Depends(get_db)]):
    # Находим покупку по ID
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()

    # Если покупка не найдена, выбрасываем исключение
    if purchase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase was not found"
        )

    # Удаляем покупку
    db.delete(purchase)
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Purchase was successfully deleted!'}
