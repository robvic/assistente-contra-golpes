import os
from openai import OpenAI


def send_message(message, history):
    client = OpenAI(api_key=os.environ.get("GPT_KEY"))

    history.append({"role": "user", "content": message})

    directive = "Você é um assistente de WhatsApp chamado Meu Netin. Seu trabalho é ajudar idosos e pessoas com pouco letramento digital a tirar dúvidas sobre golpes e fraudes digitais."
    completion = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "developer", "content": directive},{"role": "user", "content": message}]
    )

    reply = completion.choices[0].message.content

    history.append({"role": "assistant", "content": reply})

    return reply, history
