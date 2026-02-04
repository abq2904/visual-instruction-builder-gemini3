import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("API KEY FOUND:", bool(os.getenv("GEMINI_API_KEY")))

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()
for m in models:
    print(m.name, "->", m.supported_generation_methods)
