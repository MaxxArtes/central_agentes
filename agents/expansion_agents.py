from notion_client import Client
import os
from dotenv import load_dotenv

class NotionAgent:
    def __init__(self):
        """Agente para gerenciar bases de conhecimento no Notion."""
        load_dotenv()
        self.token = os.getenv("NOTION_TOKEN")
        self.notion = Client(auth=self.token) if self.token else None

    def is_active(self):
        return self.notion is not None

    def create_page(self, parent_page_id, title, content=""):
        """Cria uma nova página no Notion."""
        if not self.is_active(): return "Notion não configurado."
        try:
            new_page = self.notion.pages.create(
                parent={"page_id": parent_page_id},
                properties={"title": [{"text": {"content": title}}]},
                children=[{
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}
                }]
            )
            return f"Página '{title}' criada no Notion: {new_page['url']}"
        except Exception as e:
            return f"Erro no Notion: {str(e)}"

class TelegramAgent:
    def __init__(self):
        """Agente para comunicação via Telegram Bot."""
        load_dotenv()
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def is_active(self):
        return self.token is not None and self.chat_id is not None

    def send_message(self, text):
        """Envia mensagem simples via API do Telegram."""
        if not self.is_active(): return "Telegram não configurado."
        import requests
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": text}
        try:
            requests.post(url, json=payload)
            return "Mensagem enviada ao Telegram!"
        except Exception as e:
            return f"Erro no Telegram: {str(e)}"

class SlackAgent:
    def __init__(self):
        """Agente para integração com Slack Apps."""
        load_dotenv()
        self.token = os.getenv("SLACK_BOT_TOKEN")
        from slack_sdk import WebClient
        self.client = WebClient(token=self.token) if self.token else None

    def is_active(self):
        return self.client is not None

    def post_message(self, channel, text):
        """Posta mensagem em um canal do Slack."""
        if not self.is_active(): return "Slack não configurado."
        try:
            self.client.chat_postMessage(channel=channel, text=text)
            return f"Mensagem enviada ao canal {channel} no Slack."
        except Exception as e:
            return f"Erro no Slack: {str(e)}"

if __name__ == "__main__":
    print("Agentes de Expansão prontos (Aguardando tokens no .env)")
