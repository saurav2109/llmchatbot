import streamlit as st
from genai import get_chatbot_response
import base64

api_key = st.secrets["API_KEY"]

st.title("Zero to hero Chatbot")  # Set the title of your app

# Initialize session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Chatbot Selection in Sidebar
st.sidebar.title("Chatbot Selection")
chatbot_options = {
    "Lecture 1: The spelled-out intro to neural networks and backpropagation: building micrograd": {"image": "sources/images/image1.jpg", "transcript": "sources/transcripts/transcript1.txt", "code": "sources/codes/code1.txt"},
    "Lecture 2: The spelled-out intro to language modeling: building makemore": {"image": "sources/images/image2.jpg", "transcript": "sources/transcripts/transcript2.txt", "code": "sources/codes/code2.txt"},
    "Lecture 3: Building makemore Part 2: MLP": {"image": "sources/images/image3.jpg", "transcript": "sources/transcripts/transcript3.txt", "code": "sources/codes/code3.txt"},
    "Lecture 4: Building makemore Part 3: Activations & Gradients, BatchNorm: building minGPT": {"image": "sources/images/image4.jpg", "transcript": "sources/transcripts/transcript4.txt", "code": "sources/codes/code4.txt"},
    "Lecture 5: Building makemore Part 4: Becoming a Backprop Ninja": {"image": "sources/images/image5.jpg", "transcript": "sources/transcripts/transcript5.txt", "code": "sources/codes/code5.txt"},
    "Lecture 6: Building makemore Part 5: Building a WaveNetT": {"image": "sources/images/image6.jpg", "transcript": "sources/transcripts/transcript6.txt", "code": "sources/codes/code6.txt"},
    "Lecture 7: Let's build GPT: from scratch, in code, spelled out.": {"image": "sources/images/image7.jpg", "transcript": "sources/transcripts/transcript7.txt", "code": "sources/codes/code7.txt"},
    "Lecture 8: Let's build the GPT Tokenizer": {"image": "sources/images/image8.jpg", "transcript": "sources/transcripts/transcript8.txt", "code": "sources/codes/code8.txt"},
    "Lecture 9: Let's reproduce GPT-2 (124M)": {"image": "sources/images/image9.jpg", "transcript": "sources/transcripts/transcript9.txt", "code": "sources/codes/code9.txt"},
}

selected_chatbot = st.sidebar.selectbox("Choose a chatbot", list(chatbot_options.keys()))

# Initialize conversation history when a new chatbot is selected
if "current_chatbot" not in st.session_state or st.session_state.current_chatbot != selected_chatbot:
    st.session_state.current_chatbot = selected_chatbot
    st.session_state.conversation_history = []

# Display the selected chatbot's image
st.sidebar.image(chatbot_options[selected_chatbot]["image"], use_container_width=True)

# Display the conversation history *above* the input
st.write("##")
for i, message in enumerate(st.session_state.conversation_history):
    if message["role"] == "user":
        if 'image' in message:
            st.image(base64.b64decode(message['image']), width=200)
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "chatbot":
        st.markdown(f"**Chatbot:** {message['content']}")
st.write("---")  # Separator

# File uploader for the image
uploaded_image = st.file_uploader("Upload an image related to your question (optional)", type=["jpg", "png", "jpeg"])

# Function to handle the submission
def process_question():
    if st.session_state.question:
        image_content = None

        transcript_file = chatbot_options[selected_chatbot]["transcript"]
        code_file = chatbot_options[selected_chatbot]["code"]

        with open(transcript_file, 'r') as f:
            transcript = f.read()

        with open(code_file, 'r') as f:
            code = f.read()

        # Add user's question to the conversation history
        user_message = {"role": "user", "content": st.session_state.question}

        if uploaded_image is not None:
            image_data = uploaded_image.read()
            # Encode the image data in base64
            image_content = base64.b64encode(image_data).decode("utf-8")
            user_message["image"] = image_content
 
        st.session_state.conversation_history.append(user_message)

        # Modify get_chatbot_response to accept conversation history
        response = get_chatbot_response(
            st.session_state.question,
            transcript,
            code,
            api_key,
            image=image_content,
            conversation_history=st.session_state.conversation_history,
        )

        # Add chatbot's response to the conversation history
        st.session_state.conversation_history.append({"role": "chatbot", "content": response.text})

        # Clear the input area after submission
        st.session_state.question = ""

# Create a text input for the user to enter their question at the *bottom*
st.text_area("Ask me anything about the lecture!:", height=100, key="question")

# Use the on_click argument to trigger the processing function
col1, col2 = st.columns([3, 1])  # Adjust the ratios as needed

with col2:
    st.button("Submit", on_click=process_question)
