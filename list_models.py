# list_models.py
from google import genai

client = genai.Client()

models = client.models.list()

for m in models:
    print(m.name, m.supported_generation_methods)
