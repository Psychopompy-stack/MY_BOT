# Импорт библиотеки OpenAI для взаимодействия с OpenAI API
import openai
from business_logic.dialog_management import DialogManager
from data_access.database import get_session


def get_openai_response(prompt):
    """
    Отправляет запрос к OpenAI API с заданным текстом и возвращает ответ.

    :param prompt: Строка с текстовым запросом к модели
    :return: Текстовый ответ от модели OpenAI
    """

    # Устанавливает API-ключ для аутентификации запросов к OpenAI
    openai.api_key = "YOUR_OPENAI_API_KEY"

    # Отправляет запрос к модели text-davinci-003 с заданным prompt.
    # Параметр max_tokens ограничивает длину ответа до 150 токенов.
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    # Извлекает текст ответа из объекта response и возвращает его, удаляя лишние пробелы
    return response.choices[0].text.strip()


def chat_with_openai(dialog_id, user_id, user_message, context):
    session = get_session()
    dialog_manager = DialogManager(session)

    # Сохраняем сообщение пользователя
    dialog_manager.save_message(dialog_id, user_id, user_message)

    # Проверяем, нужно ли игнорировать старую историю
    ignore_history = context.user_data.get('ignore_history', False)

    # Получаем историю диалога
    dialog_history = dialog_manager.get_dialog_history(dialog_id)

    # Если нужно игнорировать старую историю, используем только новое сообщение
    if ignore_history:
        prompt = f":User   {user_message}\nAI:"
    else:
        # Формируем полный prompt с историей диалога и новым сообщением
        prompt = f"{dialog_history}\n:User   {user_message}\nAI:"

    # Получаем ответ от OpenAI
    response_text = get_openai_response(prompt)

    # Сохраняем ответ от OpenAI
    dialog_manager.save_message(dialog_id, user_id, response_text)

    return response_text
