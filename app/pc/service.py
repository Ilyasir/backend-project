# В этом файле будет взаимодействие с базой данных

# Импортируем базовый класс с методами
from app.services.base import BaseService

# Импортируем модели
from app.pc.models import pc

class PCService(BaseService): # Наследуемся от класса BaseService
    model = pc
    