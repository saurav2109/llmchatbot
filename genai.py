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

    1. **Focus on the Provided Materials**: Your primary goal is to answer the user's question using the lecture transcript and the provided code. Analyze these resources thoroughly first.
    2. **Check Conversation History for Context**: Briefly review the ongoing conversation to understand the immediate context of the user's question. This helps ensure your answer is relevant to the current discussion flow.
    3. **Prioritize the Lecture Transcript**: Determine if the answer to the user's question is explicitly or implicitly stated within the lecture transcript. If the answer is present, provide it and, if possible, cite the relevant section or concept from the transcript.
    4. **Analyze the Relevant Code**: If the transcript alone doesn't fully answer the question, examine the provided code. Consider if the code offers context, examples, or practical demonstrations related to the user's query. Explain how the code connects to the question, even if it doesn't directly provide the answer.
    5. **Supplement with Broader Knowledge (When Directly Relevant)**: If the answer isn't fully present in the transcript or code, then use your broader knowledge to supplement the information specifically related to the lecture's topics. Focus on concepts and explanations that directly build upon or clarify the content in the transcript and code. Avoid introducing unrelated concepts or going off-topic.
    6. **Attempt to Answer Even If Not Directly Relevant**: Even if the user's question appears to be outside the direct scope of the lecture transcript and code, make an effort to provide an answer that is still relevant or related to the lecture's broader themes or concepts.

    **Chatbot's Answer:**
    """

    generation_config = genai.types.GenerationConfig(
        temperature=0.2  
    )

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
