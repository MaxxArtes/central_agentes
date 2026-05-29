import requests
import os
from dotenv import load_dotenv

class DiscordAgent:
    def __init__(self):
        """
        Agente especializado em comunicação via Discord.
        Usa Webhooks para notificações rápidas e simples.
        """
        load_dotenv()
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def is_active(self):
        return self.webhook_url is not None and self.webhook_url != ""

    def send_message(self, message):
        """Envia uma mensagem para o canal via Webhook."""
        if not self.is_active():
            return "Erro: DISCORD_WEBHOOK_URL não configurado no .env"
        
        data = {"content": message}
        try:
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            return "Mensagem enviada ao Discord com sucesso!"
        except Exception as e:
            return f"Erro ao enviar para o Discord: {str(e)}"

    def send_embed(self, title, description, color=3447003):
        """Envia um embed (mensagem formatada) para o Discord."""
        if not self.is_active():
            return "Erro: Discord não configurado."

        data = {
            "embeds": [{
                "title": title,
                "description": description,
                "color": color
            }]
        }
        try:
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            return "Embed enviado ao Discord!"
        except Exception as e:
            return f"Erro ao enviar embed: {str(e)}"

if __name__ == "__main__":
    agent = DiscordAgent()
    if agent.is_active():
        print("Discord Agent pronto para enviar mensagens!")
    else:
        print("Configure DISCORD_WEBHOOK_URL no .env para testar.")
