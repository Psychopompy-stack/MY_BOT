from sqlalchemy.orm import Session
from datetime import datetime
from data_access.models import User, Transaction


class BalanceManager:
    def __init__(self, db: Session):
        """
        Инициализация менеджера баланса с использованием сессии базы данных.

        Args:
            db (Session): Сессия базы данных SQLAlchemy.
        """
        self.db = db

    def get_balance(self, user_id: int) -> float:
        """
        Получение текущего баланса пользователя.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            float: Текущий баланс пользователя.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            return user.balance
        raise ValueError("Пользователь не найден")

    def add_funds(self, user_id: int, amount: float) -> float:
        """
        Пополнение баланса пользователя.

        Args:
            user_id (int): Идентификатор пользователя.
            amount (float): Сумма пополнения.

        Returns:
            float: Обновлённый баланс пользователя.
        """
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше 0")

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Пользователь не найден")

        # Обновляем баланс пользователя
        user.balance += amount

        # Создаем запись о транзакции
        transaction = Transaction(
            user_id=user.id,
            amount=amount,
            transaction_type="deposit",
            timestamp=datetime.now()
        )

        # Добавляем транзакцию в базу данных
        self.db.add(transaction)
        self.db.commit()

        return user.balance

    def deduct_funds(self, user_id: int, amount: float) -> float:
        """
        Списание средств с баланса пользователя.

        Args:
            user_id (int): Идентификатор пользователя.
            amount (float): Сумма для списания.

        Returns:
            float: Обновлённый баланс пользователя.
        """
        if amount <= 0:
            raise ValueError("Сумма для списания должна быть больше 0")

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Пользователь не найден")

        if user.balance < amount:
            raise ValueError("Недостаточно средств на балансе")

        # Списываем средства с баланса пользователя
        user.balance -= amount

        # Создаем запись о транзакции
        transaction = Transaction(
            user_id=user.id,
            amount=-amount,
            transaction_type="withdrawal",
            timestamp=datetime.now()
        )

        # Добавляем транзакцию в базу данных
        self.db.add(transaction)
        self.db.commit()

        return user.balance

    def get_transaction_history(self, user_id: int):
        """
        Получение истории транзакций пользователя.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            list: Список транзакций пользователя.
        """
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id).all()

        # Формируем и возвращаем список транзакций
        return [
            {
                "amount": trans.amount,
                "type": trans.transaction_type,
                "timestamp": trans.timestamp
            }
            for trans in transactions]
