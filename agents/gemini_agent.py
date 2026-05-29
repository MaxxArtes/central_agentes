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
        try:
            try:
                from agents.openrouter_agent import OpenRouterAgent
            except ImportError:
                from openrouter_agent import OpenRouterAgent
            
            or_model = f"google/{self.model_name}"
            if "gemini-1.5-flash" in or_model: or_model = "google/gemini-2.0-flash-001"
            if "gemini-1.5-pro" in or_model: or_model = "google/gemini-pro-1.5"
            
            self.or_agent = OpenRouterAgent(model_name=or_model)
            print(f"[{self.model_name}] Usando ponte OpenRouter (Pro limits via API).")
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
            # Se falhar o login (ex: token expirado), tenta a ponte OpenRouter
            if "400" in str(e) or "401" in str(e) or "403" in str(e):
                try:
                    try:
                        from agents.openrouter_agent import OpenRouterAgent
                    except ImportError:
                        from openrouter_agent import OpenRouterAgent
                        
                    or_model = f"google/{self.model_name}"
                    if "gemini-1.5-flash" in or_model: or_model = "google/gemini-flash-1.5"
                    if "gemini-1.5-pro" in or_model: or_model = "google/gemini-pro-1.5"
                    
                    self.or_agent = OpenRouterAgent(model_name=or_model)
                    return self.or_agent.ask(prompt)
                except:
                    pass
            return f"Erro no Gemini: {str(e)}"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    agent = GeminiAgent()
    print(agent.ask("Diga 'Login Pro ativo'."))
