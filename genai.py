import google.generativeai as genai

def get_chatbot_response(question, transcript, code, api_key, image=None, conversation_history=[]):
    # Configure the API key
    genai.configure(api_key=api_key)

    # Select the Gemini Pro model
    model = genai.GenerativeModel('gemini-2.0-flash-exp')  

    lecture_transcript = transcript

    question = question

    # Format the conversation history
    history_str = ""
    if conversation_history:
        history_str = "\n**Conversation History:**\n"
        for item in conversation_history:
            role = item["role"].capitalize()
            content = item["content"]
            history_str += f"{role}: {content}\n"

    prompt = f"""**Task:** Answer the question below based on the provided lecture transcript, relevant code, and the ongoing conversation history.

    {history_str}

    **Lecture Transcript:**
    {lecture_transcript}

    **Relevant Code:**
    {code}

    **Question:** {question}

    **Reasoning Process:**

    1. **Review Conversation History:** First, check if the current question is related to previous turns in the conversation. Consider what has already been discussed.
    2. **Check the Lecture Transcript:** Determine if the answer to the question is explicitly stated in the lecture transcript. If so, provide the answer and cite the relevant portion.
    3. **Consider the Relevant Code:** If the answer isn't directly in the transcript, see if the provided code provides context or clues that can help answer the question.
    4. **Use Broader Knowledge (If Necessary):** If the answer is not found in the transcript or code, provide an informed answer based on your general knowledge, ensuring it is relevant to the lecture's topic.

    **Chatbot's Answer:**
    """

    if image:
        # Need to handle conversation history with multimodal input if the model supports it
        # Gemini Pro Vision might be required for true multimodal conversation history
        content_parts = []
        if conversation_history:
            content_parts.append(history_str)
        content_parts.append({'mime_type':'image/jpeg', 'data': image})
        content_parts.append(prompt)
        return model.generate_content(content_parts)
    else:
        return model.generate_content(prompt)
