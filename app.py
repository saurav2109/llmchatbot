import streamlit as st
from genai import get_chatbot_response  

api_key = st.secrets["API_KEY"]

with open('transcript1.txt', 'r') as f: 
    transcript = f.readlines()

with open('code1.txt', 'r') as f: 
    code = f.readlines()    

st.title("My Awesome Chatbot")  # Set the title of your app

# Create a text input for the user to enter their question
question = st.text_input("Ask me anything about the lecture:")

if question:  # If the user has entered a question
    response = get_chatbot_response(question, transcript[0], code[0], api_key)  # Call your chatbot function
    st.write("Chatbot's Answer:", response.text)  # Display the response