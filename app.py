import streamlit as st
from gemini_api import generate_instructions

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Visual Instruction Builder (Gemini)",
    layout="centered"
)

# ---------------- Custom Styling ----------------
st.markdown(
    """
    <style>
        /* App background */
        .stApp {
            background: linear-gradient(
                135deg,
                #1f103f 0%,
                #2a145c 45%,
                #351a73 100%
            );
        }

        /* Content spacing */
        .block-container {
            padding-top: 2rem;
        }

        /* Headings */
        h1, h2, h3 {
            color: #f5efff;
        }

        /* Normal text */
        p, label, div {
            color: #ece4ff;
        }

        /* Buttons — keep Streamlit behavior */
        .stButton > button {
            background-color: #6f42ff;
            color: white;
            border-radius: 10px;
            border: 1px solid #8f6bff;
        }

        .stButton > button:hover {
            background-color: #845dff;
            border-color: #a98cff;
        }

        .stButton > button:disabled {
            background-color: #3a2f66;
            color: #bfb6e5;
            border: 1px solid #5a4b8c;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Title ----------------
st.title("🧠 Visual Instruction Builder")

st.info(
    "This app uses multimodal AI to understand objects from images and generate "
    "clear, human-friendly instructions. Useful for everyday objects, tools, "
    "appliances, vehicles, and more."
)

# ---------------- Model Selection ----------------
st.subheader("🤖 Select AI Model")

model_choice = st.radio(
    "Choose which Gemini model to use for generating instructions:",
    options=["Gemini 3.0 Pro (Experimental)", "Gemini 2.5 Pro (Stable)"],
    index=0
)

st.markdown(
    "- 🚀 **Gemini 3.0 Pro**: Latest advanced reasoning and multimodal understanding\n"
    "- ⚡ **Gemini 2.5 Pro**: Stable, faster, and cost-effective alternative"
)

MODEL_MAP = {
    "Gemini 3.0 Pro (Experimental)": "models/gemini-3.0-pro-preview",
    "Gemini 2.5 Pro (Stable)": "models/gemini-2.5-pro",
}

selected_model = MODEL_MAP[model_choice]

# ---------------- Prompt Help ----------------
st.subheader("💬 What can you ask?")

st.info(
    "- ❓ *How do I use this?*\n"
    "- 🔍 *Identify this object and explain it*\n"
    "- 🛠️ *How can I fix this?*"
)

st.markdown(
    f"📌 Upload an image or paste a public image URL and describe your task.  \n"
    f"Gemini will generate clear, step-by-step instructions."
)

# ---------------- Image Input ----------------
st.subheader("📷 Image Input")

image_source = st.radio(
    "Choose image source:",
    ["Upload image", "Image URL"],
    horizontal=True
)

uploaded_image = None
image_url = None

if image_source == "Upload image":
    uploaded_image = st.file_uploader(
        "📁 Upload an image (jpg, png)",
        type=["jpg", "jpeg", "png"]
    )
else:
    image_url = st.text_input(
        "🌐 Paste a public image URL",
        placeholder="https://example.com/image.jpg"
    )

# ---------------- Task Input ----------------
st.subheader("📝 Your Task")

task = st.text_input(
    "What do you want to do with this object?",
    placeholder="e.g. How to clean this, how to assemble it, how to fix it..."
)

# ---------------- Generate Button ----------------
can_generate = (
    task and (
        uploaded_image is not None or
        (image_url and image_url.startswith("http"))
    )
)

generate_clicked = st.button(
    "✨ Generate instructions",
    disabled=not can_generate
)

# ---------------- Output ----------------
if generate_clicked:
    with st.spinner(f"🤖 Analyzing image with {model_choice}..."):
        try:
            # Attempt the selected model
            instructions = generate_instructions(
                task=task,
                model_name=selected_model,
                image_file=uploaded_image,
                image_url=image_url
            )
        except Exception as e:
            # Fallback to 2.5 Pro if 3.0 Pro fails
            if "PERMISSION_DENIED" in str(e) or "3.0" in selected_model:
                fallback_model = MODEL_MAP["Gemini 2.5 Pro (Stable)"]
                st.warning(f"⚠️ {model_choice} not available, using Gemini 2.5 Pro instead.")
                instructions = generate_instructions(
                    task=task,
                    model_name=fallback_model,
                    image_file=uploaded_image,
                    image_url=image_url
                )
                model_choice = "Gemini 2.5 Pro"
                selected_model = fallback_model
            else:
                st.error(f"❌ Error: {e}")
                instructions = None

    if instructions:
        st.subheader("📋 Step-by-Step Instructions")
        st.markdown(instructions)

        if uploaded_image:
            st.image(uploaded_image, caption="📎 Uploaded Image", width="stretch")
        else:
            st.image(image_url, caption="🌐 Image from URL", width="stretch")

        st.caption(f"🤖 Powered by Gemini")
        st.info("💡 Tip: Ask clear, concise questions for best results.")

