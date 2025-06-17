import asyncio
from nemoguardrails import LLMRails, RailsConfig

config = RailsConfig.from_path("./config")
rails = LLMRails(config)

async def stream_response(messages):
    reply = ""
    async for chunk in rails.stream_async(messages=messages):
        print(chunk, end="")
    return ""

def send_message(message, history):
    history.append({"role": "user", "content": message})

    messages=[
        {
        "role":"developer",
        "content":"Você é um assistente de WhatsApp chamado Meu Netin. Seu trabalho é ajudar idosos e pessoas com pouco letramento digital a tirar dúvidas sobre golpes e fraudes digitais."
        },
        {
        "role": "user",
        "content": message
        }]

    reply = asyncio.run(stream_response(messages))

    history.append({"role": "assistant", "content": reply})

    return reply, history

if __name__ == "__main__":
    history = []
    message = "Olá, quem é você?"
    reply, history = send_message(message, history)
    print(reply)