# В этом файле будет взаимодействие с базой данных

# Импортируем базовый класс с методами
from app.services.base import BaseService

# Импортируем модели
from app.userPc.models import UserPc

class UserPcService(BaseService): # Наследуемся от класса BaseService
    model = UserPc
    