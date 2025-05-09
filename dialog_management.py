from sqlalchemy.orm import Session
from data_access.models import Dialog, GPTMessage
from datetime import datetime


class DialogManager:
    def __init__(self, session: Session):
        self.session = session

    def create_dialog(self, user_id: int, bot_type: str, role_type: str) -> int:
        """Создает новый диалог для пользователя и возвращает его ID."""
        new_dialog = Dialog(
            user_id=user_id,
            bot_type=bot_type,
            role_type=role_type,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(new_dialog)
        self.session.commit()
        return new_dialog.dialog_id

    def update_dialog(self, dialog_id: int, bot_type: str = None, role_type: str = None, dialog_vol: int = None):
        """Обновляет существующий диалог по его ID."""
        # Получаем существующий диалог по его ID
        dialog = self.session.query(Dialog).filter(Dialog.dialog_id == dialog_id).first()

        # Проверяем, существует ли диалог
        if not dialog:
            raise ValueError("Dialog not found")

        # Обновляем поля диалога, если соответствующие параметры были переданы
        if bot_type is not None:
            dialog.bot_type = bot_type
        if role_type is not None:
            dialog.role_type = role_type
        if dialog_vol is not None:
            dialog.dialog_vol = dialog_vol

        self.session.commit()

    def save_message(self, dialog_id: int, user_id: int, message_text: str):
        """
        Сохраняет сообщение в базе данных.

        :param dialog_id: Идентификатор диалога
        :param user_id: Идентификатор пользователя
        :param message_text: Текст сообщения
        """

        try:
            new_message = GPTMessage(dialog_id=dialog_id, user_id=user_id, message_text=message_text)
            self.session.add(new_message)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при сохранении сообщения: {e}")
        finally:
            self.session.close()

    def get_dialog_history(self, dialog_id: int):
        """
        Извлекает историю сообщений для данного диалога.

        :param dialog_id: Идентификатор диалога
        :return: Строка с историей сообщений
        """

        try:
            messages = self.session.query(GPTMessage).filter(GPTMessage.dialog_id == dialog_id).order_by(
                GPTMessage.message_time).all()
            history = "\n".join(
                [f":User  {msg.message_text}" if msg.user_id else f"AI: {msg.message_text}" for msg in messages])
            return history
        finally:
            self.session.close()

    def get_user_dialogs(self, user_id: int):
        """Получает все диалоги для указанного пользователя."""
        return self.session.query(Dialog).filter(Dialog.user_id == user_id).all()

    def get_dialog_by_id(self, dialog_id: int):
        """Извлекает диалог по его ID."""
        return self.session.query(Dialog).filter(Dialog.dialog_id == dialog_id).first()
