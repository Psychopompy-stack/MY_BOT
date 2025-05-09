from data_access.database import init_db
from dialogs import handle_create_dialog_settings

# Настройка логирования.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Инициализация логгера с использованием имени текущего модуля.
logger = logging.getLogger(__name__)


# Определение команд
def main():

    """
    Создаем Updater и передаем ему токен
    Updater - это основной класс для работы с Telegram API. Он управляет соединением с API и отправляет обновления (updates) боту.
    """
    application = Application.builder().token("7672229960:AAGJ3nYrvj_LG9Gzu_UfsS-PsV4K3p1T0yE").build()

    """
    Регистрация обработчиков команд
    Обработчики команд связывают текстовые команды с соответствующими функциями.
    Когда пользователь вводит команду (например, /start), соответствующая функция будет вызвана.
    """
    application.add_handler(CommandHandler("start", start))          # Обработчик для команды /start
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_create_dialog_settings,
                                                 pattern='start_dialog_settings'))
    application.add_handler(CallbackQueryHandler(set_role_callback, pattern=r'^(role_1|role_2)_[0-9]+$'))
    # Обработчик для выбора модели
    application.add_handler(CallbackQueryHandler(handle_create_dialog_settings,
                                                 pattern='^(gpt_4o_create|gpt_4o_mini_create|o1_create|o1_mini_create)$'))

    application.add_handler(CallbackQueryHandler(button_callback))

    # updater.start_polling()
    application.run_polling()


if __name__ == '__main__':
    """
    Этот блок кода проверяет, выполняется ли данный файл как основная программа.
    Специальная переменная __name__ в Python указывает на имя текущего модуля.
    Если модуль запущен напрямую (например, через python bot.py), __name__ будет равно '__main__'.
    Если же модуль импортируется из другого файла, __name__ будет равно имени этого модуля.
    """

    """
    Вызов функции main() запускает выполнение программы.
    В данном случае, функция main() инициализирует и запускает Telegram-бота.
    """
    init_db()
    main()
