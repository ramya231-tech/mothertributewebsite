# app.py
import streamlit as st
import os
from database import *
from datetime import datetime

from transformers import pipeline
from PIL import Image

st.set_page_config(page_title="Mother's Day Tribute", layout="centered")

# Initialize DB tables
create_tribute_table()
create_wisdom_table()

# Load AI caption model
@st.cache_resource

def load_caption_model():
    return pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
caption_model = load_caption_model()

st.title("💐 Mother's Day Tribute Site")

menu = ["Submit Tribute", "View Tributes", "Mom Wisdom Wall", "Surprise Tribute Generator"]
page = st.sidebar.selectbox("Menu", menu)

# Page 1: Submit Tribute
if page == "Submit Tribute":
    st.header("📝 Submit Your Tribute")
    name = st.text_input("Your Name")
    tribute = st.text_area("Your Tribute Message")
    image = st.file_uploader("Upload a photo of Mom (optional)", type=['jpg', 'jpeg', 'png'])

    if st.button("Submit Tribute"):
        image_path = ""
        caption = ""
        if image:
            os.makedirs("uploads", exist_ok=True)
            image_path = os.path.join("uploads", image.name)
            with open(image_path, "wb") as f:
                f.write(image.getbuffer())
            caption = caption_model(Image.open(image_path))[0]['generated_text']

        if name and tribute:
            insert_tribute(name, tribute, image_path, caption)
            st.success("Tribute submitted successfully!")
        else:
            st.error("Please provide your name and tribute message.")

# Page 2: View Tributes
elif page == "View Tributes":
    st.header("💖 View Submitted Tributes")
    results = get_all_tributes()
    for r in results:
        st.subheader(f"From: {r[1]}")
        st.write(r[2])
        if r[3]:
            st.image(r[3], use_container_width=True)
        if r[4]:
            st.caption(f"AI Caption: {r[4]}")
        st.markdown("---")

# Page 3: Mom Wisdom Wall
elif page == "Mom Wisdom Wall":
    st.header("🧠 Mom Wisdom Wall")
    user_name = st.text_input("Your Name")
    mom_quote = st.text_area("Share a life lesson or quote from your mom")
    if st.button("Submit Wisdom"):
        if user_name and mom_quote:
            insert_wisdom(user_name, mom_quote)
            st.success("Wisdom submitted successfully!")
        else:
            st.error("Please fill in all fields.")
    st.markdown("### 🌟 Shared Wisdom")
    wisdom_entries = get_all_wisdom()
    for entry in wisdom_entries:
        st.write(f"**{entry[1]}** says: \"{entry[2]}\"")

# Page 4: Surprise Tribute Generator
elif page == "Surprise Tribute Generator":
    st.header("🎁 Surprise Tribute Generator")
    mom_name = st.text_input("Mom's Name")
    quality = st.text_input("Her best quality")
    memory = st.text_area("A cherished memory with her")
    if st.button("Generate Tribute"):
        if mom_name and quality and memory:
            tribute = f"Dear {mom_name},\n\nYour {quality} has always been a guiding light in my life. I still remember {memory}. Thank you for everything. Happy Mother's Day!\n\nWith love."
            st.markdown("### 💖 Your Generated Tribute")
            st.write(tribute)
        else:
            st.error("Please fill in all fields.")
