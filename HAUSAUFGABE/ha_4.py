import time
from google import genai
from dotenv import load_dotenv
import os
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
import requests

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

def handle_rate_limit_error(e):
    """
    Обработчик ошибки, если API вернуло превышение лимита запросов.
    """
    if isinstance(e, requests.exceptions.HTTPError):
        if e.response.status_code == 429:
            print("Превышен лимит скорости, повторная попытка")
            return True
    return False

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3), retry=handle_rate_limit_error)
def get_gemini_response(prompt):
    """
    Отправляет запрос к модели Gemini и возвращает текст ответа.

    :param prompt: Текст запроса.
    :return: Текст ответа модели.
    """
    time.sleep(0.3)  # Небольшая задержка перед отправкой запроса (можно убрать или изменить)

    # Используем глобальный объект клиента
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt],
        )
        return response.text
    except requests.exceptions.Timeout:
        print("Время ожидания запроса истекло.")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Запрос не выполнен: {e}.")
        raise


#Пример использования
if __name__== "__main__":
    try:
        response = get_gemini_response("Что такое лимиты запросов?")
        print(response)
    except RetryError:
        print("Достигнуто максимальное количество попыток. Пожалуйста, повторите попытку позже.")



































#Вот как можно реализовать защиту от блокировок API, обработку таймаутов и retry-механизм с использованием библиотеки tenacity в Python:
#
#🔧 Установка tenacity
#Если ещё не установлен:
#
#
#pip install tenacity
#📦 Пример реализации с requests и tenacity
#
#import requests
#from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
#from requests.exceptions import Timeout, HTTPError, ConnectionError
#
## ✅ Retry-декоратор
#@retry(
#    retry=retry_if_exception_type((Timeout, ConnectionError, HTTPError)),
#    stop=stop_after_attempt(5),  # Максимум 5 попыток
#    wait=wait_exponential(multiplier=1, min=2, max=10),  # Экспоненциальная задержка
#)
#def fetch_data_from_api(url, params=None, headers=None):
#    try:
#        response = requests.get(url, params=params, headers=headers, timeout=5)
#        response.raise_for_status()  # выбрасывает HTTPError при плохом статусе
#        return response.json()
#    except Timeout:
#        print("⏱️ Таймаут! Повтор запроса...")
#        raise
#    except HTTPError as e:
#        if response.status_code == 429:
#            print("🚫 Превышен лимит запросов (Rate Limit).")
#        raise
#    except ConnectionError:
#        print("🔌 Проблема с соединением.")
#        raise
#
## 🔄 Использование
#if __name__ == "__main__":
#    try:
#        data = fetch_data_from_api("https://api.example.com/data")
#        print(data)
#    except Exception as e:
#        print(f"❌ Ошибка при получении данных: {e}")
##🧠 Что реализовано:
##Retry-механизм с tenacity, который:
##
##Повторяет запрос при таймауте, сетевых ошибках или HTTP ошибках.
##
##Использует экспоненциальную задержку между повторами.
##
##Обработка HTTP 429 (rate limit) с выводом сообщения.
##
##Обработка таймаутов и ConnectionError'ов.
##
##Хочешь, могу помочь адаптировать это под твой текущий проект — просто покажи код API-запроса, с которым работаешь.