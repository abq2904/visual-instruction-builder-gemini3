import os
import requests
from io import BytesIO
from PIL import Image
from google import genai


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    return genai.Client(api_key=api_key)


def load_image(image_file=None, image_url=None) -> Image.Image:
    """
    Load image from uploaded file or public URL.
    """
    if image_file:
        return Image.open(image_file).convert("RGB")

    if image_url:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")

    raise ValueError("No image source provided")


def generate_instructions(
    task: str,
    model_name: str,
    image_file=None,
    image_url=None
) -> str:
    client = get_client()
    image = load_image(image_file=image_file, image_url=image_url)

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
        model=model_name,
        contents=[
            image,
            system_prompt,
            f"Task: {task}"
        ]
    )

    return response.text
