from sqlalchemy import Column, Integer, String, DECIMAL, Text, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from .db import Base, SessionLocal, engine  # импортируем Base, SessionLocal, engine из модуля db


class Buyer(Base):
    __tablename__ = 'sqlalchemy_buyer'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False)
    age = Column(Integer, nullable=False)
    slug = Column(String, unique=True, index=True)

    # Добавляем отношение с каскадным удалением
    purchases = relationship("Purchase", cascade="all, delete-orphan", back_populates="buyer")


    def __repr__(self):
        return f'Buyer(name={self.name}, balance={self.balance}, age={self.age})'


class Medicine(Base):
    __tablename__ = 'sqlalchemy_medicine'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    cost = Column(DECIMAL(6, 2), nullable=False)
    description = Column(Text, nullable=False)
    age_limited = Column(Boolean, default=False)
    slug = Column(String, unique=True, index=True)

    # Добавляем отношение с каскадным удалением
    purchases = relationship("Purchase", cascade="all, delete-orphan", back_populates="medicine")


    def __repr__(self):
        return (f'Medicine(title={self.title}, category={self.category}, cost={self.cost}, '
                f'description={self.description}, age_limited={self.age_limited})')


class Purchase(Base):
    __tablename__ = 'sqlalchemy_purchase'
    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey('sqlalchemy_buyer.id'), nullable=False)
    medicine_id = Column(Integer, ForeignKey('sqlalchemy_medicine.id'), nullable=False)
    date = Column(DateTime, nullable=False)

    # Добавляем обратные отношения
    buyer = relationship("Buyer", back_populates="purchases")
    medicine = relationship("Medicine", back_populates="purchases")

    def __repr__(self):
        return f'Purchase(buyer_id={self.buyer_id}, medicine_id={self.medicine_id}, date={self.date})'


# Создаём таблицы после определения моделей
Base.metadata.create_all(engine)

