import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()
TELEFONE_CONTACT = "11948525402"
CONTACT_NAME = "EasyScheduling"

class MessageSender:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        # self.api_key = os.environ.get('API_KEY')
        self.send_message_url = "http://whatsapp_web_api:3000/client/sendMessage/f8377d8d-a589-4242-9ba6-9486a04ef80c"
        self.check_number_url = "http://whatsapp_web_api:3000/client/getNumberId/f8377d8d-a589-4242-9ba6-9486a04ef80c"
        self.headers = {
            'accept': '*/*',
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def clean_phone_number(self, telefone):
        try:
            return re.sub(r'\D', '', telefone)
        except Exception as e:
            print(f"Erro ao limpar número de telefone: {e}")
            return None

    def check_number(self, telefone):
        try:
            cleaned_phone = self.clean_phone_number(telefone)
            payload = {"number": f"55{cleaned_phone}"}
            response = requests.post(self.check_number_url, headers=self.headers, json=payload)
            response_data = response.json()
            if response_data.get("success") and "result" in response_data and "_serialized" in response_data["result"]:
                return response_data["result"]["_serialized"]
        except Exception as e:
            print(f"Erro ao verificar número: {e}")
        return None

    def send_message(self, telefone, texto):
        try:
            serialized_phone = self.check_number(telefone)
            if not serialized_phone:
                return {"error": "Número de telefone não possui WhatsApp ou não é válido."}
            payload = {
                "chatId": serialized_phone,
                "contentType": "string",
                "content": texto
            }
            response = requests.post(self.send_message_url, headers=self.headers, json=payload)
            return response.json()
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return None
    
    def send_contact(self, telefone_user, telefone_contact):
        try:
            serialized_phone_user = self.check_number(telefone_user)
            if not serialized_phone_user:
                return {"error": "Número de telefone do usuário não possui WhatsApp ou não é válido."}
            serialized_phone_contact = self.check_number(telefone_contact)
            if not serialized_phone_contact:
                return {"error": "Número de telefone do contato não possui WhatsApp ou não é válido."}
            payload = {
                "chatId": serialized_phone_user,
                "contentType": "Contact",
                "content": {"contactId": serialized_phone_contact}
            }
            response = requests.post(self.send_message_url, headers=self.headers, json=payload)
            return response.json()
        except Exception as e:
            print(f"Erro ao enviar contato: {e}")
            return None
