"""
Импорт классов для определения столбцов в моделях базы данных:
  Column - базовый класс для создания столбцов
  Integer, String, DateTime, Boolean, Float - типы данных для столбцов
  ForeignKey - используется для создания внешнего ключа, связывающего таблицы
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON

# Импорт функции relationship для установления отношений между таблицами
from sqlalchemy.orm import relationship

# Импорт базового класса Base, который используется для определения всех моделей
from data_access.database import Base

# Импорт datetime для работы с датой и временем
from datetime import datetime

"""
Общий комментарий:
  Один к одному - Каждая запись в первой таблице соответствует ровно одной записи во второй таблице
  Один ко многим - Каждая запись в первой таблице может соответствовать нескольким записям во второй таблице
"""


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    user_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship('Subscription', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')
    balance_history = relationship('BalanceHistory', back_populates='user')
    user_balances = relationship('UserBalance', back_populates='user')
    dialogs = relationship('Dialog', back_populates='user')
    dalle_messages = relationship('DALLEMessage', back_populates='user')
    gpt_messages = relationship('GPTMessage', back_populates='user')


class Subscription(Base):
    __tablename__ = 'subscriptions'

    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    subscription_type = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    conditions = Column(JSON)

    user = relationship('User', back_populates='subscriptions')


class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    transaction_sum = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    transaction_description = Column(String, nullable=True)

    user = relationship('User', back_populates='transactions')


class BalanceHistory(Base):
    __tablename__ = 'balance_history'

    history_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    balance_sum = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='balance_history')


class UserBalance(Base):
    __tablename__ = 'user_balances'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    balance_id = Column(Integer, primary_key=True)
    up_date = Column(DateTime, default=datetime.utcnow)
    balance_now = Column(Float, nullable=False)

    user = relationship('User', back_populates='user_balances')


class Dialog(Base):
    __tablename__ = 'dialogs'

    dialog_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    bot_type = Column(String, nullable=False)
    role_type = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='dialogs')
    gpt_messages = relationship('GPTMessage', back_populates='dialog')
    dalle_messages = relationship('DALLEMessage', back_populates='dialog')


class DALLEMessage(Base):
    __tablename__ = 'dalle_messages'

    message_id = Column(Integer, primary_key=True)
    dialog_id = Column(Integer, ForeignKey('dialogs.dialog_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    message_time = Column(DateTime, default=datetime.utcnow)
    message_text = Column(String, nullable=False)
    dalle_image = Column(String, nullable=True)

    dialog = relationship('Dialog', back_populates='dalle_messages')
    user = relationship('User', back_populates='dalle_messages')


class GPTMessage(Base):
    __tablename__ = 'gpt_messages'

    message_id = Column(Integer, primary_key=True)
    dialog_id = Column(Integer, ForeignKey('dialogs.dialog_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    message_time = Column(DateTime, default=datetime.utcnow)
    message_text = Column(String, nullable=False)

    dialog = relationship('Dialog', back_populates='gpt_messages')
    user = relationship('User', back_populates='gpt_messages')
