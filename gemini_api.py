import os
from PIL import Image
from google import genai


MODEL_NAME = "models/gemini-2.5-pro"  # Tier 1 compatible


def get_client():
    """
    Lazily initialize the Gemini client to avoid failures at import time.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    return genai.Client(api_key=api_key)


def generate_instructions(image_file, task: str) -> str:
    """
    Generate step-by-step visual instructions for a given image and user task.
    """
    client = get_client()
    image = Image.open(image_file)

    system_prompt = (
        "You are an expert visual instructor.\n\n"
        "You are given:\n"
        "1) An image of a real-world object\n"
        "2) A user task describing what they want to do with the object\n\n"
        "Your job:\n"
        "- Carefully analyze the object in the image\n"
        "- Understand the user's intent\n"
        "- Generate clear, step-by-step instructions\n"
        "- Use simple language\n"
        "- Assume the user is a beginner\n"
        "- Mention safety warnings if relevant\n"
        "- Do NOT hallucinate tools or parts that are not visible\n\n"
        "Output format:\n"
        "- Short title\n"
        "- Numbered steps\n"
        "- Optional safety note at the end"
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            image,
            system_prompt,
            f"Task: {task}"
        ]
    )

    # Optional debug info (safe if unavailable)
    token_usage = getattr(response, "token_usage", None)
    if token_usage:
        print("Tokens used:", token_usage)
    else:
        print("Tokens used: N/A")

    return response.text
