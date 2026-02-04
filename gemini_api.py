import os
from dotenv import load_dotenv
from PIL import Image
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-2.5-pro"  # now OK with Tier 1


def generate_instructions(image_file, task: str) -> str:
    image = Image.open(image_file)

    system_prompt = """
    You are an expert visual instructor.

    You are given:
    1) An image of a real-world object
    2) A user task describing what they want to do with the object

    Your job:
    - Carefully analyze the object in the image
    - Understand the user's intent
    - Generate clear, step-by-step instructions
    - Use simple language
    - Assume the user is a beginner
    - Mention safety warnings if relevant
    - Do NOT hallucinate tools or parts that are not visible

    Output format:
    - Short title
    - Numbered steps
    - Optional safety note at the end
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            image,
            system_prompt,
            f"Task: {task}"
        ]
    )

    # Optional logging
    print("Tokens used:", response.token_usage if hasattr(response, "token_usage") else "N/A")
    
    return response.text
