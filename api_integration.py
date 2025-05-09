# Импорт библиотеки openai для взаимодействия с OpenAI API
import openai

# Импорт библиотеки requests для отправки HTTP-запросов
import requests

# Импорт типов для аннотации типов в функции
from typing import Dict, Any

# Импорт функции get_session из модуля database
from data_access.database import get_session

# Импорт модели ImageRequest из модуля models
from data_access.models import ImageRequest

# Импорт класса datetime из модуля datetime
from datetime import datetime


class APIIntegration:
    def __init__(self, openai_api_key: str, dalle_api_key: str):
        """
        Инициализация интеграции с API.

        Args:
            openai_api_key (str): API-ключ для OpenAI.
            dalle_api_key (str): API-ключ для DALL-E.
        """
        openai.api_key = openai_api_key
        self.dalle_api_key = dalle_api_key

    @staticmethod
    def generate_text(prompt: str, model: str = "text-davinci-003") -> str:
        """
        Генерация текста с использованием OpenAI GPT.

        Args:
            prompt (str): Текстовый запрос для генерации.
            model (str): Модель для генерации текста.

        Returns:
            str: Сгенерированный текст.
        """
        try:
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Ошибка при генерации текста: {e}")
            return ""

    def generate_image(self, prompt: str) -> str:
        """
        Генерация изображения с использованием DALL-E.

        Args:
            prompt (str): Описание изображения для генерации.

        Returns:
            str: URL сгенерированного изображения.
        """
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {self.dalle_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "image-alpha-001",
            "prompt": prompt,
            "num_images": 1
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            image_url = response_data['data'][0]['url']
            self.save_image_request(prompt, image_url)
            return image_url
        except Exception as e:
            print(f"Ошибка при генерации изображения: {e}")
            return ""

    @staticmethod
    def save_image_request(prompt: str, image_url: str):
        """
        Сохраняет запрос на генерацию изображения в базу данных.

        Args:
            prompt (str): Описание изображения.
            image_url (str): URL сгенерированного изображения.
        """
        session = get_session()
        image_request = ImageRequest(
            user_id=1,  # Здесь можно указать реального пользователя, если требуется
            prompt_text=prompt,
            image_url=image_url,
            timestamp=datetime.now()
        )

        session.add(image_request)
        session.commit()
