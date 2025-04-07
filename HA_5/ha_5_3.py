import os  # Модуль для работы с операционной системой (например, для работы с переменными окружения).
from dotenv import load_dotenv  # Функция для загрузки переменных окружения из файла .env.
from langchain_community.document_loaders import PyPDFLoader  # Импортируем загрузчик для PDF-файлов.
from langchain_core.vectorstores import InMemoryVectorStore  # Импортируем класс для создания векторного хранилища в памяти.
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # Импортируем класс для генерации эмбеддингов с использованием Google Generative AI.
from langchain_google_genai import ChatGoogleGenerativeAI  # Импортируем класс для работы с моделью Google Generative AI.
from langchain.chains.question_answering import load_qa_chain  # Импортируем цепочку для вопрос-ответа.

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем API-ключ из переменной окружения "GEMINI_API_KEY"
api_key = os.getenv("GEMINI_API_KEY")

# Если переменная "GOOGLE_API_KEY" не установлена, присваиваем ей значение из GEMINI_API_KEY
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = api_key

# Выводим сообщение о начале чтения PDF-файла
print('Start reading..')

# Создаем объект загрузчика для указанного PDF-файла
loader = PyPDFLoader('romeo-and-juliet.pdf')  # Укажите путь к вашему PDF-файлу
pages = loader.load()  # Загружаем страницы из PDF

# Выводим сообщение о начале формирования эмбеддингов
print('Start embedding..')

# Создаем векторное хранилище, преобразуя документы (страницы PDF) в эмбеддинги.
# Для генерации эмбеддингов используется модель GoogleGenerativeAIEmbeddings с указанной моделью "models/embedding-001".
vector_store = InMemoryVectorStore.from_documents(pages, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

# Выполняем поиск документов по смысловому запросу.
# Функция similarity_search ищет наиболее похожие страницы по заданному запросу.
query = "Romeo gets poisoned"
docs = vector_store.similarity_search(query, k=2)

# Инициализируем модель Google Generative AI для генерации ответов
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key, temperature=0.7)

# Загружаем цепочку для вопрос-ответа
qa_chain = load_qa_chain(llm, chain_type="stuff")

# Генерируем ответ на основе найденных документов
response = qa_chain.run(input_documents=docs, question=query)

# Выводим результаты
print('=' * 30)
print(f"Вопрос: {query}")
print(f"Ответ: {response}")
print('=' * 30)

# Перебираем найденные документы и выводим номер страницы и содержание.
for doc in docs:
    print('=' * 30)
    print(f'Page {doc.metadata["page"]}: {doc.page_content}\n')
    print('+' * 30)