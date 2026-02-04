import streamlit as st
from gemini_api import generate_instructions

st.set_page_config(
    page_title="Visual Instruction Builder (Gemini 3)",
    layout="centered"
)

st.title("🧠 Visual Instruction Builder")
st.info(
    "This app uses multimodal AI to understand objects from images and generate "
    "clear, human-friendly instructions. Useful for everyday objects, tools, "
    "appliances, vehicles, and more."
)
st.markdown(
    "**Try prompts like:**\n"
    "- *How do I use this?*\n"
    "- *Identify this object and explain it*\n"
    "- *How can I fix this?*\n"
)
st.write(
    "Upload an image of any object and describe what you want to do. "
    "Gemini 3 will generate step-by-step instructions."
)

uploaded_image = st.file_uploader(
    "Upload an image (jpg, png)",
    type=["jpg", "jpeg", "png"]
)

task = st.text_input(
    "What do you want to do with this object?",
    placeholder="e.g. How to clean this, how to assemble it, how to fix it..."
)

generate_clicked = st.button(
    "Generate instructions",
    disabled=not (uploaded_image and task)
)

if generate_clicked:
    with st.spinner("Analyzing the image and generating instructions..."):
        instructions = generate_instructions(uploaded_image, task)

    st.subheader("📋 Step-by-Step Instructions")
    st.markdown(instructions)

    st.image(
        uploaded_image,
        caption="Uploaded Image",
        width="stretch"
    )
    
    st.caption("🤖 Powered by the all new Gemini 3")
    st.info("Tip: Ask clear, concise questions for best results.")

    

