import google.generativeai as genai

def get_chatbot_response(question, transcript, code, api_key, image=None):
    # Configure the API key
    genai.configure(api_key=api_key)

    # Select the Gemini Pro model (free tier)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    lecture_transcript = transcript

    question = question

    prompt = f"""**Task:** Answer the question below based on the provided lecture transcript and relevant code.

    **Lecture Transcript:**
    {lecture_transcript}

    **Relevant Code:**
    {code}

    **Question:** {question}

    **Reasoning Process:**

    1. **Check the Lecture Transcript:** First, determine if the answer to the question is explicitly stated in the lecture transcript. If so, provide the answer and cite the relevant portion.
    2. **Consider the Relevant Code:** If the answer isn't directly in the transcript, see if the provided code provides context or clues that can help answer the question.
    3. **Use Broader Knowledge (If Necessary):** If the answer is not found in the transcript or code, provide an informed answer based on your general knowledge, ensuring it is relevant to the lecture's topic.

    **Chatbot's Answer:**
    """

    if image:
        return model.generate_content([{'mime_type':'image/jpeg', 'data': image}, prompt])
    else:
        return model.generate_content(prompt)

if __name__ == "__main__":
    pass