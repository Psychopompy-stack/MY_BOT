# Импорт класса Session из SQLAlchemy
# Создает сессии, которые используются для управления базой данных
from sqlalchemy.orm import Session

# Импорт модели User из файла models
from data_access.models import User

# Optional — тип аннотации из стандартной библиотеки Python, указывает, что значение либо указанного типа, либо None
from typing import Optional

# datetime — класс из стандартной библиотеки Python, который используется для работы с датами и временем
from datetime import datetime


class UserManager:
    """
    Менеджер для управления пользователями в базе данных.
    """

    def __init__(self, db: Session):
        """
        Инициализация менеджера пользователей с использованием сессии базы данных.

        Args:
            db (Session): Сессия базы данных SQLAlchemy.
        """
        self.db = db  # Сохраняем сессию базы данных для использования в методах

    def register_user(self, user_name: str, telegram_id: str) -> User:
        """
        Регистрация нового пользователя в базе данных.

        Args:
            user_name (str): Имя пользователя.
            telegram_id (str): Идентификатор Telegram пользователя.

        Returns:
            User: Объект зарегистрированного пользователя.
        """
        # Проверяем, существует ли уже пользователь с данным telegram_id
        existing_user = self.db.query(User).filter(User.telegram_id == telegram_id).first()

        if existing_user:
            raise ValueError("Пользователь с таким telegram_id уже существует")

        # Создаем нового пользователя
        new_user = User(
            user_name=user_name,  # Устанавливаем имя пользователя
            telegram_id=telegram_id,  # Устанавливаем идентификатор Telegram
            created_at=datetime.now()  # Устанавливаем текущую дату и время
        )

        # Добавляем нового пользователя в сессию и сохраняем изменения в базе данных
        self.db.add(new_user)
        self.db.commit()

        return new_user  # Возвращаем зарегистрированного пользователя

    def update_username(self, user_id: int, new_user_name: str) -> Optional[User]:
        """
        Обновление имени пользователя в базе данных.

        Args:
            user_id (int): Идентификатор пользователя.
            new_user_name (str): Новое имя пользователя.

        Returns:
            Optional[User ]: Обновленный объект пользователя или None, если пользователь не найден.
        """
        # Находим пользователя по user_id
        user = self.db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise ValueError("Пользователь не найден")

        # Обновляем имя пользователя
        user.user_name = new_user_name

        # Сохраняем изменения в базе данных
        self.db.commit()

        return user  # Возвращаем обновленного пользователя

    def get_user_by_telegram_id(self, telegram_id: str) -> Optional[User]:

        """
        Получение пользователя по telegram_id.
        
        Args:
            telegram_id (str): Идентификатор Telegram пользователя.
            
        Returns:
            Optional[User ]: Объект пользователя или None, если пользователь не найден.
        """

        # Запрашиваем пользователя по telegram_id
        user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
        return user  # Возвращаем найденного пользователя

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Получение пользователя по ID.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            Optional[User ]: Объект пользователя или None, если пользователь не найден.
        """
        # Запрашиваем пользователя по user_id
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

    def delete_user(self, user_id: int) -> bool:
        """
        Удаление пользователя из базы данных.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            bool: True, если пользователь был успешно удален, иначе False.
        """
        # Находим пользователя по user_id
        user = self.db.query(User).filter(User.user_id == user_id).first()

        if user:
            # Удаляем пользователя из базы данных
            self.db.delete(user)
            self.db.commit()
            return True  # Возвращаем True, если удаление прошло успешно

        return False  # Возвращаем False, если пользователь не найден
