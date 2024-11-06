# Настройки соединения с базой данных

TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres:Zaq12wsX@localhost:5432/ShopPG"
    },
    "apps": {
        "models": {
            "models": ["models"],  # Указываем путь к моделям
            "default": True,
        }
    }
}
