import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def categorize_text_with_llm(extracted_text: str) -> str:
    prompt = (
        "Classify the following LinkedIn post as one of: "
        "1. Job search strategy\n"
        "2. Resource/reference\n"
        "3. Job post\n\n"
        f"Text: \"{extracted_text}\"\n"
        "Respond with only the category name."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        temperature=0
    )
    return response.choices[0].message.content.strip()
