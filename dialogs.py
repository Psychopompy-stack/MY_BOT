from telegram import Update
from telegram.ext import CallbackContext
from keyboard import (
    main_menu_keyboard, buy_menu_keyboard, dialog_menu_keyboard, subscriptions_keyboard, create_dialog_keyboard,
    dialog_settings_keyboard, choose_dialog_keyboard, mode_choose_keyboard, dialog_create_model_choose_keyboard,
    dialog_create_role_choose_keyboard, model_choose_keyboard, ddddd_keyboard, dialog_change_role_choose_keyboard
)
import logging
from data_access.database import get_session
from business_logic.user_management import UserManager
from handlers import (
    handle_create_dialog_settings, create_dialog_list, handle_subscription_1, handle_button_click,
    set_role_callback, handle_model_choose_keyboard
)

# Определяем этапы
SELECT_MODEL, SELECT_ROLE = range(2)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: CallbackContext):

    # Получаем идентификатор пользователя и имя пользователя из обновления
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Неизвестный пользователь"

    # Получаем сессию базы данных
    session = get_session()
    user_manager = UserManager(session)

    try:
        # Пробуем зарегистрировать пользователя
        new_user = user_manager.register_user(user_name=username, telegram_id=user_id)
        # Отправляем приветственное сообщение пользователю
        await update.message.reply_text(f"Добро пожаловать, {new_user.user_name}! Вы успешно зарегистрированы.")
    except ValueError as e:
        # Обработка ошибки, если пользователь уже существует
        await update.message.reply_text(f"Ошибка: {str(e)}")
    finally:
        session.close()

    # Предлагаем пользователю выбрать опцию из основного меню

    await update.message.reply_text("Выберите опцию:", reply_markup=main_menu_keyboard())


async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Обязательно отвечаем на запрос

    # Если выбрали диалог, извлекаем dialog_id
    if query.data.startswith('dialog_'):
        dialog_id = query.data.split('_')[1]  # Извлекаем ID диалога
        context.user_data['current_dialog_id'] = dialog_id  # Сохраняем dialog_id в контексте

        # Переходим к следующей клавиатуре
        await query.edit_message_text("Выберите действие для диалога:", reply_markup=ddddd_keyboard())
        return

    # Словарь для сопоставления данных кнопок с действиями
    actions = {
        'buy': lambda: query.edit_message_text("Выберите действие:",
                                               reply_markup=buy_menu_keyboard()),
        'create_choose_dialog': lambda: query.edit_message_text('че то там',
                                                                reply_markup=dialog_menu_keyboard()),

        'subscriptions': lambda: query.edit_message_text('че то там',
                                                        reply_markup=subscriptions_keyboard()),

        'create_dialog': lambda: handle_create_dialog_settings(update, context),
        'choose_dialog': lambda: create_dialog_list(update, context),

        'basic': lambda: handle_subscription_1(update, context),
        'premium': lambda: handle_subscription_1(update, context),
        'unlimited': lambda: handle_subscription_1(update, context),

        'conduct_dialog': lambda: query.edit_message_text('че то там',
                                                          reply_markup=mode_choose_keyboard()),
        'settings_dialog': lambda: query.edit_message_text('че то там',
                                                           reply_markup=dialog_settings_keyboard()),
        'reset_dialog': lambda: query.edit_message_text('че то там',
                                                        reply_markup=handle_button_click(update, context)),

        'text': lambda: query.edit_message_text('ведение диалога'),
        'image': lambda: query.edit_message_text('ведение диалога'),

        'model_choose': lambda: query.edit_message_text('че то там',
                                                        reply_markup=model_choose_keyboard()),
        'role_choose': lambda: query.edit_message_text('че то там',
                                                       reply_markup=dialog_change_role_choose_keyboard(context.user_data.get('current_dialog_id'))),

        'gpt_4o_mini_create': lambda: handle_create_dialog_settings(update, context),
        'gpt_4o_create': lambda: handle_create_dialog_settings(update, context),
        'o1_mini_create': lambda: handle_create_dialog_settings(update, context),
        'o1_create': lambda: handle_create_dialog_settings(update, context),

        'gpt_4o_mini': lambda: handle_model_choose_keyboard(update, context),
        'gpt_4o': lambda: handle_model_choose_keyboard(update, context),
        'o1_mini': lambda: handle_model_choose_keyboard(update, context),
        'o1': lambda: handle_model_choose_keyboard(update, context),

        'role_1': lambda: set_role_callback(update, context),
        'role_2': lambda: set_role_callback(update, context)
    }

    # Получаем действие из словаря по значению query.data, если оно существует
    action = actions.get(query.data)

    # Если действие найдено, выполняем его
    if action:
        await action()
    elif query.data.startswith('dialog_'):
        dialog_id = query.data.split('_')[1]  # Извлекаем ID диалога
        context.user_data['current_dialog_id'] = dialog_id  # Сохраняем dialog_id в контексте

        # Переходим к следующей клавиатуре
        await query.edit_message_text("Выберите действие для диалога:", reply_markup=ddddd_keyboard())
        return
    else:
        await query.edit_message_text("Неизвестное действие")  # Обработка случая, если действие не найдено
