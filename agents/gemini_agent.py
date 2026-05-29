import google.generativeai as genai
import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class GeminiAgent:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model_name = model_name
        self.authenticated = False
        
        # 1. Tentar carregar tokens da Gemini CLI (npx gemini)
        # PRIORIDADE MÁXIMA: Usar sua conta logada (Pro)
        if self._setup_cli_auth():
            print(f"[{model_name}] Autenticado via Gemini CLI (Pro Access).")
            self.authenticated = True
        
        # 2. Se falhar, tentar Application Default Credentials (gcloud)
        if not self.authenticated:
            try:
                genai.configure()
                print(f"[{model_name}] Autenticado via Google Cloud CLI (ADC).")
                self.authenticated = True
            except Exception:
                pass
        
        # 3. Se falhar, tentar API Key do .env
        if not self.authenticated:
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if api_key:
                # Limpa configurações anteriores para evitar conflito credentials vs api_key
                genai.configure(api_key=api_key)
                print(f"[{model_name}] Autenticado via API Key.")
                self.authenticated = True
        
        if not self.authenticated:
            print(f"[{model_name}] Aviso: Nenhuma forma de autenticação encontrada.")
        
        self.model = genai.GenerativeModel(model_name)

    def _setup_cli_auth(self):
        """Tenta localizar e carregar o token da Gemini CLI."""
        token_path = os.path.join(os.environ['USERPROFILE'], '.gemini', 'oauth_creds.json')
        if not os.path.exists(token_path):
            return False
        
        try:
            # Importante: Garantir que não há API_KEY no ambiente que cause conflito
            if "GOOGLE_API_KEY" in os.environ: del os.environ["GOOGLE_API_KEY"]
            if "GEMINI_API_KEY" in os.environ: del os.environ["GEMINI_API_KEY"]

            with open(token_path, "r") as f:
                creds_data = json.load(f)
            
            creds = Credentials(
                token=creds_data.get("access_token"),
                refresh_token=creds_data.get("refresh_token"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=None, 
                client_secret=None
            )
            
            # Tenta configurar o SDK globalmente usando as credenciais do npx gemini
            # Forçamos api_key como None para evitar o erro de exclusividade mútua
            genai.configure(credentials=creds, api_key=None)
            return True
        except Exception as e:
            print(f"Erro ao carregar token da CLI: {e}")
            return False
    
    def ask(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao processar requisição: {str(e)}"

if __name__ == "__main__":
    # Teste rápido
    from dotenv import load_dotenv
    load_dotenv()
    try:
        agent = GeminiAgent()
        print(agent.ask("Olá, quem é você? Responda em uma frase curta."))
    except Exception as e:
        print(e)
