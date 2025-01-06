import google.generativeai as genai

def get_chatbot_response(question, transcript, code, api_key, image=None):
    # Configure the API key
    genai.configure(api_key=api_key)

    # Select the Gemini Pro model (free tier)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    lecture_transcript = transcript

    question = question

    prompt = f"""Here is the lecture transcript: '{lecture_transcript}',
    and here is the relevant code: '{code}'. 
    Answer the following question based on the provided lecture transcript. If the answer can be found within the transcript, please use that information and show it as well as proof. If the answer is not directly in the transcript, provide an informed response based on your broader knowledge, but make sure your answer is relevant and related to the topic of the transcript: '{question}'. 
    Chatbot's Answer: """

    if image:
        return model.generate_content([{'mime_type':'image/jpeg', 'data': image}, prompt])
    else:
        return model.generate_content(prompt)

if __name__ == "__main__":
    pass