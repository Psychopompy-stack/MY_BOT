from telegram import Update
from telegram.ext import (CallbackContext)
from keyboard import (
    dialog_create_model_choose_keyboard, dialog_create_role_choose_keyboard, choose_dialog_keyboard,
    create_dialog_keyboard
)
from data_access.database import get_session
from business_logic.user_management import UserManager
from business_logic.dialog_management import DialogManager
from business_logic.subscription_management import SubscriptionManager


async def handle_create_dialog_settings(update: Update, context: CallbackContext):
    """
    Обрабатывает клавиатуру с настройками

    :param update: Update
    :param context: CallbackContext
    :return: InlineKeyboardMarkup, Message
    """

    query = update.callback_query
    await query.answer()  # Обязательно отвечаем на callback_query

    # Проверяем, что это первый вызов функции
    if query.data == 'create_dialog':  # Предположим, что это действие для начала
        await query.edit_message_text("Выберите модель:", reply_markup=dialog_create_model_choose_keyboard())
    else:
        # Получаем выбранную модель
        selected_model = query.data
        context.user_data['selected_model'] = selected_model  # Сохраняем выбор модели для дальнейшего использования

        # Предлагаем выбрать роль
        await query.edit_message_text("Выберите роль:", reply_markup=dialog_create_role_choose_keyboard())


async def create_dialog_list(update: Update, context: CallbackContext):
    """
    Выводит клавиатуру со списком диалогов пользователя

    :param update: Update
    :param context: CallbackContext
    :return: InlineKeyboardMarkup, Message
    """

    telegram_id = str(update.effective_user.id)
    session = get_session()
    user_manager = UserManager(session)
    user = user_manager.get_user_by_telegram_id(telegram_id)
    user_id = user.user_id

    # Создаем клавиатуру
    keyboard = choose_dialog_keyboard(user_id)

    # Отправляем клавиатуру пользователю
    await update.callback_query.message.reply_text("Выберите диалог:", reply_markup=keyboard)


async def handle_subscription_1(update: Update, context: CallbackContext):
    """
    Осуществляет добавление подписки

    :param update: Update
    :param context: CallbackContext
    :return: Message
    """

    query = update.callback_query
    plan = query.data

    # Получение user_id (id telegram)
    telegram_id = str(update.effective_user.id)

    # Начало сессии БД
    session = get_session()

    # Объект менеджера пользователя
    user_manager = UserManager(session)
    # Получение пользователя по telegram_id
    user = user_manager.get_user_by_telegram_id(telegram_id)
    user_id = user.user_id

    # Объект менеджера подписок
    sub_manager = SubscriptionManager(session)
    sub = sub_manager.has_active_subscription(user_id, plan=plan)

    # Если подписка есть - удалить и добавить новую, если нет - добавить новую
    if sub == True:
        sub_manager.remove_subscription(user_id)
        sub_manager.add_subscription(user_id, plan, 30)
    else:
        sub_manager.add_subscription(user_id, plan, 30)

    session.commit()
    session.close()

    query = update.callback_query
    await query.edit_message_text("Подписка 1")


def handle_button_click(update: Update, context: CallbackContext):
    """
    Осуществляет сброс контекста

    :param update: Update
    :param context: CallbackContext
    :return: InlineKeyboardMarkup, Message
    """

    query = update.callback_query
    query.answer()

    if query.data == 'dialog_reset':
        # Сбрасываем контекст
        context.user_data['ignore_history'] = True
        query.edit_message_text(text="Контекст сброшен. Вы можете начать новый диалог.",
                                reply_markup=create_dialog_keyboard())
    else:
        # Обработка других кнопок
        query.edit_message_text(text=f"Вы нажали кнопку: {query.data}", reply_markup=create_dialog_keyboard())


async def set_role_callback(update: Update, context: CallbackContext):
    """
    Осуществляет выбор роли

    :param update: Update
    :param context: CallbackContext
    :return: Message
    """

    query = update.callback_query
    await query.answer()

    # Извлекаем dialog_id и выбранную роль
    dialog_id = context.user_data.get('current_dialog_id')
    if not dialog_id:
        await query.edit_message_text("Ошибка: ID диалога не найден.")
        return

    parts = query.data.split('_')
    if len(parts) < 3:
        await query.edit_message_text("Ошибка: некорректный формат callback_data.")
        return

    role_prefix, selected_role, dialog_id = parts
    selected_role = f"{role_prefix}_{selected_role}"  # Получим, например, "role_1".

    # Обновляем роль в базе данных
    session = get_session()
    dialog_manager = DialogManager(session)
    dialog_manager.update_dialog(dialog_id=dialog_id, role_type=selected_role)

    await query.edit_message_text(f"Роль для диалога {dialog_id} изменена на: {selected_role}.")


async def handle_model_choose_keyboard(update: Update, context: CallbackContext):
    """
    Осуществляет выбор модели

    :param update: Update
    :param context: CallbackContext
    :return: Message
    """

    query = update.callback_query
    await query.answer()

    # Извлекаем dialog_id и выбранную модель
    dialog_id = context.user_data.get('current_dialog_id')
    if not dialog_id:
        await query.edit_message_text("Ошибка: ID диалога не найден.")
        return

    parts = query.data.split('_')
    if len(parts) < 2:
        await query.edit_message_text("Ошибка: некорректный формат callback_data.")
        return

    model_prefix, selected_model = parts
    selected_model = f"{model_prefix}_{selected_model}"  # Например, "model_1".

    # Получаем информацию о пользователе
    telegram_id = str(update.effective_user.id)
    session = get_session()
    user_manager = UserManager(session)
    user = user_manager.get_user_by_telegram_id(telegram_id)
    user_id = user.user_id

    # Получаем диалоги пользователя
    dialog_manager = DialogManager(session)
    dialogs = dialog_manager.get_user_dialogs(user_id)

    if not dialogs:
        await query.edit_message_text("Ошибка: диалоги пользователя не найдены.")
        return

    dialog = dialogs[0]  # Предполагаем, что мы берем первый диалог
    dialog_id = dialog.dialog_id

    # Обновляем диалог с выбранной моделью
    dialog_manager.update_dialog(dialog_id=dialog_id, bot_type=selected_model)

    await query.edit_message_text(f"Выбрана модель: {selected_model} для диалога {dialog_id}.")
