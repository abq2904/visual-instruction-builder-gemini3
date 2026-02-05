# list_models_fixed.py
from google import genai

client = genai.Client()

models = client.models.list()

print("Available models in this SDK:")
for m in models:
    # print whatever attributes exist
    print("Model name:", getattr(m, "name", "N/A"))
    print("Description:", getattr(m, "description", "N/A"))
    print("Capabilities:", getattr(m, "capabilities", "N/A"))
    print("----")
