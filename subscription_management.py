# Импортируем класс Session из модуля sqlalchemy.orm
from sqlalchemy.orm import Session

# Импортируем datetime и timedelta из модуля datetime
from datetime import datetime, timedelta

# Импортируем модели Subscription и User из модуля models
from data_access.models import Subscription, User


class SubscriptionManager:
    """
    Менеджер для управления подписками пользователей в базе данных.
    """

    def __init__(self, db: Session):
        """
        Инициализация менеджера подписок с использованием сессии базы данных.

        Args:
            db (Session): Сессия базы данных SQLAlchemy.
        """
        self.db = db  # Сохраняем сессию базы данных для использования в методах

    @staticmethod
    def get_conditions(self, subscription_type):
        # Определение условий для каждой подписки
        conditions = {
            "basic": {
                "duration": 30,  # Длительность подписки в днях
                "max_requests": 100,  # Максимальное количество запросов
                "features": ["basic_model"]  # Доступные функции
            },
            "premium": {
                "duration": 90,
                "max_requests": 500,
                "features": ["premium_model", "image_generation"]  # Дополнительные функции
            },
            "unlimited": {
                "duration": 365,
                "max_requests": None,  # Без ограничений
                "features": ["premium_model", "image_generation", "priority_support"]
            },
        }
        return conditions.get(subscription_type, {})

    def add_subscription(self, user_id: int, plan: str, duration_days: int) -> str:
        """
        Добавляет новую подписку пользователю в базу данных.

        Args:
            user_id (int): Уникальный идентификатор пользователя.
            plan (str): Тип подписки, которую нужно добавить.
            duration_days (int): Продолжительность подписки в днях.

        Returns:
            str: Результат операции.
        """
        # Проверяем, существует ли уже подписка для данного пользователя и плана
        existing_subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()

        if existing_subscription:
            return f"Подписка '{plan}' уже существует для пользователя с ID {user_id}."

        # Получаем условия для подписки
        conditions = self.get_conditions(self, subscription_type=plan)

        # Устанавливаем дату начала и окончания подписки
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)

        # Создаем новую подписку с условиями
        new_subscription = Subscription(
            user_id=user_id,
            subscription_type=plan,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=conditions["duration"]),
            conditions=conditions  # Сохраняем условия в формате JSON
        )

        # Добавляем новую подписку в сессию и сохраняем изменения в базе данных
        self.db.add(new_subscription)
        self.db.commit()
        return f"Подписка '{plan}' добавлена пользователю с ID {user_id}."

    def remove_subscription(self, user_id: int) -> str:
        """
        Удаляет подписку у пользователя из базы данных.

        Args:
            user_id (int): Уникальный идентификатор пользователя.

        Returns:
            str: Результат операции.
        """
        # Находим подписку по user_id и plan
        subscription = self.db.query(Subscription).filter(Subscription.user_id == user_id).first()

        if subscription:
            # Удаляем подписку из базы данных
            self.db.delete(subscription)
            self.db.commit()
            return f"Подписка '{subscription}' удалена для пользователя с ID {subscription}."

        return f"Подписка '{subscription}' не найдена у пользователя с ID {subscription}."

    def get_subscriptions(self, user_id: int) -> list:
        """
        Возвращает список всех подписокл пользователя.

        Args:
            user_id (int): Уникальный идентификатор пользователя.

        Returns:
            list: Список подписок пользователя.
        """
        # Запрашиваем все подписки пользователя
        subscriptions = self.db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).all()

        # Формируем и возвращаем список подписок с необходимыми данными
        return [{
            "plan": sub.plan,
            "start_date": sub.start_date,
            "end_date": sub.end_date
        } for sub in subscriptions]

    def has_active_subscription(self, user_id: int, plan: str) -> bool:
        """
        Проверяет, есть ли у пользователя активная подписка определенного типа.

        Args:
            user_id (int): Уникальный идентификатор пользователя.
            plan (str): Тип подписки для проверки.

        Returns:
            bool: True, если подписка активна, иначе False.
        """
        # Проверяем наличие активной подписки
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.end_date > datetime.now()
        ).first()

        return subscription is not None  # Возвращаем True, если подписка найдена

    def renew_subscription(self, user_id: int, plan: str, duration_days: int) -> str:
        """
        Продлевает подписку пользователя.

        Args:
            user_id (int): Уникальный идентификатор пользователя.
            plan (str): Тип подписки, которую нужно продлить.
            duration_days (int): Продолжительность продления в днях.

        Returns:
            str: Результат операции.
        """
        # Находим подписку по user_id и plan
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.plan == plan
        ).first()

        if subscription:
            # Если подписка активна, продлеваем ее
            if subscription.end_date > datetime.now():
                subscription.end_date += timedelta(days=duration_days)
            else:
                # Если подписка неактивна, обновляем даты
                subscription.start_date = datetime.now()
                subscription.end_date = subscription.start_date + timedelta(days=duration_days)

            # Сохраняем изменения в базе данных
            self.db.commit()
            return f"Подписка '{plan}' продлена для пользователя с ID {user_id}."

        return f"Подписка '{plan}' не найдена у пользователя с ID {user_id}."
