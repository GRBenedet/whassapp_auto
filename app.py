import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
print("OPENAI_API_KEY:", OPENAI_API_KEY)  # Depuração
print("TWILIO_WHATSAPP_NUMBER:", TWILIO_WHATSAPP_NUMBER)  # Depuração

# Configurar chaves da API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Inicializar o cliente da OpenAI
openai.api_key = OPENAI_API_KEY

# Criar a aplicação Flask
app = Flask(__name__)

# Rota para receber mensagens do WhatsApp
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    # Capturar a mensagem recebida
    incoming_msg = request.values.get("Body", "").strip()
    sender_number = request.values.get("From", "")
    
    # Criar resposta do Twilio
    response = MessagingResponse()
    msg = response.message()
    
    if not incoming_msg:
        msg.body("Não entendi a sua mensagem. Pode repetir?")
        return str(response)
    
    # Enviar a mensagem para o ChatGPT
    chatgpt_response = chatgpt_query(incoming_msg)
    
    # Enviar a resposta para o WhatsApp
    msg.body(chatgpt_response)
    return str(response)


def chatgpt_query(prompt):
    """Envia a mensagem para o ChatGPT e retorna a resposta."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou "gpt-4" se sua chave permitir
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Desculpe, houve um erro ao processar sua mensagem."

# Iniciar a API
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
