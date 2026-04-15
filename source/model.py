from openai import OpenAI
client = OpenAI()

def query_model(prompt: str, token_limit: int = 512) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=512,
    )
    return response.choices[0].message.content