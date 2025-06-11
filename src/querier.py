import os
from openai import OpenAI


def send_message(message):
    client = OpenAI(api_key=os.environ.get("GPT_KEY"))
    directive = "Você é um assistente de WhatsApp chamado Meu Netin. Seu trabalho é ajudar idosos e pessoas com pouco letramento digital a tirar dúvidas sobre golpes e fraudes digitais."
    completion = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "developer", "content": directive},{"role": "user", "content": message}]
    )

    return completion.choices[0].message.content
