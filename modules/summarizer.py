import google.generativeai as genai

def summarize_feedback(feedback_list, api_key):
    # Set up Gemini API
    genai.configure(api_key=api_key)

    # Combine all feedback into a single string
    combined_feedback = "\n".join(feedback_list)

    # Prepare the prompt
    prompt = f"Summarize the following viewer feedback clearly and concisely:\n\n{combined_feedback}"

    # Use the free-tier Gemini model
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    # Generate the summary
    response = model.generate_content(prompt)

    return response.text