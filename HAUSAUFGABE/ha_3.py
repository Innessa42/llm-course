
from google import genai
import os, random
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

message = "Привет ИИ!"

response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message)

print(response.text)
