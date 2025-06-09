import os
from openai import OpenAI


def send_message(message):
    client = OpenAI(api_key=os.environ.get("GPT_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": message}]
    )

    return completion.choices[0].message.content