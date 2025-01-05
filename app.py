import streamlit as st
from genai import get_chatbot_response  
import base64

api_key = st.secrets["API_KEY"]

st.title("Zero to hero Chatbot")  # Set the title of your app

# Chatbot Selection in Sidebar
st.sidebar.title("Chatbot Selection")
chatbot_options = {
    "Lecture 1: The spelled-out intro to neural networks and backpropagation: building micrograd": {"image": "sources/images/image1.jpg", "transcript": "sources/transcript1.txt", "code": "sources/code1.txt"},
    "Lecture 2: The spelled-out intro to language modeling: building makemore": {"image": "sources/images/image2.jpg", "transcript": "sources/transcript2.txt", "code": "sources/code2.txt"},
    # Add more chatbots as needed
}

selected_chatbot = st.sidebar.selectbox("Choose a chatbot", list(chatbot_options.keys()))

# Display the selected chatbot's image
st.sidebar.image(chatbot_options[selected_chatbot]["image"], use_container_width=True)

# File uploader for the image
uploaded_image = st.file_uploader("Upload an image related to your question (optional)", type=["jpg", "png", "jpeg"])

# Create a text input for the user to enter their question
question = st.text_area("Ask me anything about the lecture:", height=100)  # Set a fixed height (e.g., 100 pixels)

submitted = st.button("Submit")  # Add a submit button
if submitted:
    if question:

        image_content = None
        if uploaded_image is not None:
            image_data = uploaded_image.read()
            transcript_file = chatbot_options[selected_chatbot]["transcript"]
            code_file = chatbot_options[selected_chatbot]["code"]

            with open(transcript_file, 'r') as f: 
                transcript = f.readlines()

            with open(code_file, 'r') as f: 
                code = f.readlines()    

            # Encode the image data in base64
            image_content = base64.b64encode(image_data).decode("utf-8")

            # Display the base64-encoded image (for example, in an HTML img tag)
            html_code = f'<img src="data:image/jpeg;base64,{image_content}" alt="Uploaded Image"/>'
            st.markdown(html_code, unsafe_allow_html=True)

        response = get_chatbot_response(question, transcript[0], code[0], api_key, image=image_content)
        st.write("Chatbot's Answer:", response.text)