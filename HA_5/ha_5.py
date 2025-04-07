#Функция для создания цепочки, которая объединяет документы и обрабатывает их с помощью LLM.
from langchain.chains.combine_documents import create_stuff_documents_chain
#Класс для создания шаблонов промптов для чата.
from langchain_core.prompts import ChatPromptTemplate
#Класс для работы с генеративной моделью от Google.
from langchain_google_genai import ChatGoogleGenerativeAI
#Класс для загрузки документов (в данном случае – веб-страницы).
from langchain_community.document_loaders import WebBaseLoader
#Модуль для работы с переменными окружения (из файла .env).
from dotenv import load_dotenv
#Модуль для работы с операционной системой (например, для получения переменных окружения).
import os

#Загружаем переменные окружения из файла .env. Это нужно, чтобы получить секретные ключи, не прописывая их в коде.
load_dotenv()
user_agent = os.getenv("USER_AGENT")
api_key = os.getenv("GEMINI_API_KEY")

os.environ["USER_AGENT"] = user_agent
#Инициализация модели Google Gemini с ключом API
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

#Создание загрузчика для скачивания веб-страницы
loader = WebBaseLoader("https://habr.com/ru/companies/cian/articles/892650/")

#Загрузка документа с веб-страницы
docs = loader.load()

#Создание шаблона для промпта
prompt = ChatPromptTemplate.from_template("Напишите краткое изложение следующего текста: {context}")

#Создание цепочки для обработки документов
chain = create_stuff_documents_chain(llm, prompt)

#Запуск цепочки с переданным документом
try:
    result = chain.invoke({"context": docs})

    # Красивый вывод результата
    print("=" * 50)
    for text in result.split('.'):
        print(text)
    print("=" * 50)
except Exception as e:
    print(f"Ошибка: {e}")