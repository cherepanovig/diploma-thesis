from fastapi import FastAPI
from PG_Django.sqlalchemy_shop.Routers.route import router_b as buyer_router  # Импортируем роутер из route.py
from PG_Django.sqlalchemy_shop.Routers.route import router_m as medicine_router  # Импортируем роутер из route.py
from PG_Django.sqlalchemy_shop.Routers.route import router_p as purchase_router  # Импортируем роутер из route.py


# Создаем экземпляр приложения FastAPI
app = FastAPI(title="Аптека API",
              description="API SQLAlchemy для управления аптекой",
              version="1.0.0")


# Маршрут для корневого пути '/'
@app.get('/')
async def welcome():
    return {"message": "Welcome!"}


# Подключаем маршруты
app.include_router(buyer_router)

# Подключаем маршруты
app.include_router(medicine_router)

# Подключаем маршруты
app.include_router(purchase_router)
