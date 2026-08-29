from ollama import chat


def ask_llm(question, data=None):

    if data is None:

        prompt = f"""
You are a helpful AI business assistant.

Answer the user's question clearly and simply.

User question:
{question}
"""

    else:

        prompt = f"""
You are an AI business data analyst.

Answer the user's question using ONLY the data provided below.

User question:
{question}

Data:
{data}

Do not invent numbers.
If the data does not contain enough information, say so clearly.
"""

    response = chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]