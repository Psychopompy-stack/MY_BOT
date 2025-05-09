from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from business_logic.dialog_management import DialogManager
from business_logic.user_management import UserManager
from data_access.database import get_session
from telegram.ext import CallbackContext


def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Купить", callback_data='buy')],
        [InlineKeyboardButton("Создать/настроить диалог", callback_data='create_choose_dialog')]
    ]
    return InlineKeyboardMarkup(keyboard)


def buy_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('Подписки', callback_data='subscriptions')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)


def dialog_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('Создать диалог', callback_data='create_dialog')],
        [InlineKeyboardButton('Выбрать диалог', callback_data='choose_dialog')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)


def subscriptions_keyboard():
    keyboard = [
        [InlineKeyboardButton('Подписка База', callback_data='basic')],
        [InlineKeyboardButton('Подписка Премиум', callback_data='premium')],
        [InlineKeyboardButton('Подписка Безлимит', callback_data='unlimited')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)


def create_dialog_keyboard():
    keyboard = [
        [InlineKeyboardButton('Настроить диалог', callback_data='dialog_settings')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)


def dialog_settings_keyboard():
    keyboard = [
        [InlineKeyboardButton('Выбор модели', callback_data='model_choose')],
        [InlineKeyboardButton('Выбор роли', callback_data='role_choose')],
        [InlineKeyboardButton('Объем диалога', callback_data='dialog_volume')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)


def dialog_create_model_choose_keyboard():
    keyboard = [
        [InlineKeyboardButton('GPT 4o', callback_data='gpt_4o_create')],
        [InlineKeyboardButton('GPT 4o mini', callback_data='gpt_4o_mini_create')],
        [InlineKeyboardButton('o1', callback_data='o1_create')],
        [InlineKeyboardButton('o1 mini', callback_data='o1_mini_create')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)


def dialog_create_role_choose_keyboard():
    keyboard = [
        [InlineKeyboardButton('Роль 1', callback_data='role_1_create')],
        [InlineKeyboardButton('Роль 2', callback_data='role_2_create')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)


def dialog_change_role_choose_keyboard(dialog_id: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton('Роль 1', callback_data=f'role_1_{dialog_id}')],
        [InlineKeyboardButton('Роль 2', callback_data=f'role_2_{dialog_id}')],
        [InlineKeyboardButton('Назад', callback_data=f'back_{dialog_id}')]
    ]
    return InlineKeyboardMarkup(keyboard)


def model_choose_keyboard():
    keyboard = [
        [InlineKeyboardButton('GPT 4o', callback_data='gpt_4o')],
        [InlineKeyboardButton('GPT 4o mini', callback_data='gpt_4o_mini')],
        [InlineKeyboardButton('o1', callback_data='o1')],
        [InlineKeyboardButton('o1 mini', callback_data='o1_mini')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)


def choose_dialog_keyboard(user_id: int) -> InlineKeyboardMarkup:
    session = get_session()  # Получаем сессию
    dialog_manager = DialogManager(session)
    keyboard = []

    # Получаем диалоги пользователя
    user_dialogs = dialog_manager.get_user_dialogs(user_id)

    # Проверяем, есть ли диалоги
    if not user_dialogs:
        return InlineKeyboardMarkup([])  # Возвращаем пустую клавиатуру, если нет диалогов

    for index, dialog in enumerate(user_dialogs):
        title = dialog.title if hasattr(dialog, 'title') else "Без названия"
        button = InlineKeyboardButton(text=f"Диалог {index + 1}: {title}", callback_data=f"dialog_{dialog.dialog_id}")
        keyboard.append([button])  # Добавляем кнопку в строку

    return InlineKeyboardMarkup(keyboard)


def mode_choose_keyboard():
    keyboard = [
        [InlineKeyboardButton('Текст', callback_data='text')],
        [InlineKeyboardButton('Изображения', callback_data='image')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)


def ddddd_keyboard():
    keyboard = [
        [InlineKeyboardButton('Ведение диалога', callback_data='conduct_dialog')],
        [InlineKeyboardButton('Настроить диалог', callback_data='settings_dialog')],
        [InlineKeyboardButton('Сбросить диалог', callback_data='reset_dialog')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)
