import google.generativeai as genai

def ask_question(question, context_slides, api_key):
    # Configure Gemini API
    genai.configure(api_key=api_key)

    # Combine the context slides
    context_text = "\n\n".join([f"{s['title']}:\n{s['content']}" for s in context_slides])
    prompt = f"Use the following context to answer the question.\n\nContext:\n{context_text}\n\nQuestion: {question}"

    # Use the free-tier supported model
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    # Generate content
    response = model.generate_content(prompt)
    print(response.text)

    return response.text


# AIzaSyDJqd-MKCmdTMZgaS5F7FhW-SB9e3Svexw