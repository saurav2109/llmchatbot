import streamlit as st
from genai import get_chatbot_response  
import base64

api_key = st.secrets["API_KEY"]

with open('sources/transcript1.txt', 'r') as f: 
    transcript = f.readlines()

with open('sources/code1.txt', 'r') as f: 
    code = f.readlines()    

st.title("Zero to hero Chatbot")  # Set the title of your app

# Create a text input for the user to enter their question
question = st.text_input("Ask me anything about the lecture:")

# File uploader for the image
uploaded_image = st.file_uploader("Upload an image related to your question (optional)", type=["jpg", "png", "jpeg"])

if question:
    image_content = None
    if uploaded_image is not None:
        image_data = uploaded_image.read()

        # Encode the image data in base64
        image_content = base64.b64encode(image_data).decode("utf-8")

        # Display the base64-encoded image (for example, in an HTML img tag)
        html_code = f'<img src="data:image/jpeg;base64,{image_content}" alt="Uploaded Image"/>'
        st.markdown(html_code, unsafe_allow_html=True)

    response = get_chatbot_response(question, transcript[0], code[0], api_key, image=image_content)
    st.write("Chatbot's Answer:", response.text)