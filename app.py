import streamlit as st
from gemini_api import generate_instructions

st.set_page_config(
    page_title="Visual Instruction Builder (Gemini 3)",
    layout="centered"
)

st.title("🧠 Visual Instruction Builder")
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

if uploaded_image and task and st.button("Generate instructions"):
    with st.spinner("Analyzing image and generating steps..."):
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

    

