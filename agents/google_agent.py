import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

class GoogleAgent:
    def __init__(self):
        """
        Agente especializado no ecossistema Google Workspace.
        Tenta reaproveitar o login do Gemini CLI.
        """
        load_dotenv()
        self.creds = self._load_creds()
        self.drive_service = build('drive', 'v3', credentials=self.creds) if self.creds else None
        self.docs_service = build('docs', 'v1', credentials=self.creds) if self.creds else None

    def _load_creds(self):
        token_path = os.path.join(os.environ['USERPROFILE'], '.gemini', 'oauth_creds.json')
        if os.path.exists(token_path):
            with open(token_path, "r") as f:
                data = json.load(f)
            return Credentials(
                token=data.get("access_token"),
                refresh_token=data.get("refresh_token"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=os.getenv("GOOGLE_CLIENT_ID"), # Opcional se já estiver no token
                client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
            )
        return None

    def is_active(self):
        return self.drive_service is not None

    def list_drive_files(self, page_size=10):
        if not self.is_active(): return "Google Drive não autenticado."
        try:
            results = self.drive_service.files().list(
                pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                return "Nenhum arquivo encontrado no Drive."
            return [f"{item['name']} ({item['id']})" for item in items]
        except Exception as e:
            return f"Erro no Drive: {str(e)}"

    def create_doc(self, title, content=""):
        if not self.is_active(): return "Google Docs não autenticado."
        try:
            body = {'title': title}
            doc = self.docs_service.documents().create(body=body).execute()
            doc_id = doc.get('documentId')
            
            if content:
                requests = [{'insertText': {'location': {'index': 1}, 'text': content}}]
                self.docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
            
            return f"Documento '{title}' criado. ID: {doc_id}"
        except Exception as e:
            return f"Erro ao criar Doc: {str(e)}"

if __name__ == "__main__":
    agent = GoogleAgent()
    if agent.is_active():
        print("Conectado ao Google Workspace!")
        print("Arquivos recentes:", agent.list_drive_files())
    else:
        print("Aguardando autenticação Google...")
