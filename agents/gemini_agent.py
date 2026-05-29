from google import genai
from google.genai import types
import os
import json
from google.oauth2.credentials import Credentials

class GeminiAgent:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model_name = model_name
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        # REMOVE CHAVES DO AMBIENTE PARA EVITAR O ERRO 400 (API KEY INVALID)
        if "GOOGLE_API_KEY" in os.environ: del os.environ["GOOGLE_API_KEY"]
        if "GEMINI_API_KEY" in os.environ: del os.environ["GEMINI_API_KEY"]
        
        token_path = os.path.join(os.environ['USERPROFILE'], '.gemini', 'oauth_creds.json')
        
        # 1. Tentar usar o login do npx gemini
        if os.path.exists(token_path):
            try:
                with open(token_path, "r") as f:
                    data = json.load(f)
                
                creds = Credentials(
                    token=data.get("access_token"),
                    refresh_token=data.get("refresh_token"),
                    token_uri="https://oauth2.googleapis.com/token"
                )
                
                self.client = genai.Client(credentials=creds, http_options={'api_version': 'v1beta'})
                print(f"[{self.model_name}] Conta Pro detectada (Login CLI).")
                return
            except Exception as e:
                print(f"Aviso: Falha ao carregar login: {e}")

        # 2. Ponte de Emergência via OpenRouter
        self._setup_openrouter_bridge()

    def _setup_openrouter_bridge(self):
        try:
            try:
                from agents.openrouter_agent import OpenRouterAgent
            except ImportError:
                from openrouter_agent import OpenRouterAgent
            
            # Deixa o OpenRouterAgent lidar com o mapeamento de IDs
            self.or_agent = OpenRouterAgent(model_name=self.model_name)
            print(f"[{self.model_name}] Usando ponte OpenRouter.")
        except Exception as e:
            print(f"Erro ao inicializar ponte: {e}")

    def ask(self, prompt):
        if hasattr(self, 'or_agent'):
            return self.or_agent.ask(prompt)
            
        if not self.client:
            return "Erro: Sistema não autenticado. Por favor, rode 'npx gemini' no seu terminal."
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            # Se falhar o login, tenta a ponte OpenRouter imediatamente
            print(f"Erro no login nativo: {e}. Mudando para OpenRouter...")
            self._setup_openrouter_bridge()
            if hasattr(self, 'or_agent'):
                return self.or_agent.ask(prompt)
            return f"Erro fatal: {str(e)}"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    agent = GeminiAgent()
    print(agent.ask("Olá!"))
