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

    1. **Check Conversation History for Context**: Briefly review the ongoing conversation to understand the immediate context of the user's question. This helps ensure your answer is relevant to the current discussion flow.
    2. **Analyze the Lecture Transcript and Code**: Determine if the answer to the user's question is explicitly or implicitly stated within the lecture transcript and/or code. If the answer is present, provide it and, if possible, cite the relevant section.
    3. **Attempt to Answer Even If Not Directly Relevant**: Even if the user's question appears to be outside the direct scope of the lecture transcript and code, provide an answer that is still relevant or related to the lecture's broader themes or concepts.

    **Chatbot's Answer:**
    """

    generation_config = genai.types.GenerationConfig(
        temperature=0.2  
    )
    # past image will not be passed into conversation history
    if image:
        content_parts = []
        if conversation_history:
            content_parts.append(history_str)
        content_parts.append({'mime_type':'image/jpeg', 'data': image})
        content_parts.append(prompt)
        response = model.generate_content(content_parts, generation_config=generation_config)
    else:
        response = model.generate_content(prompt, generation_config=generation_config)

    return response
