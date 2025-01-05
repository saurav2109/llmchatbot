import google.generativeai as genai

def get_chatbot_response(question, transcript, code, api_key):
    # Configure the API key
    genai.configure(api_key=api_key)

    # Select the Gemini Pro model (free tier)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    lecture_transcript = transcript

    question = question

    prompt = f"""Here is the lecture transcript: '{lecture_transcript}',
    and here is the relevant code: '{code}'. 
    Answer the following question based on the provided lecture transcript: '{question}'. 
    Chatbot's Answer: """

    return model.generate_content(prompt)

if __name__ == "__main__":
    print(get_chatbot_response("What is the lecture about?").text)