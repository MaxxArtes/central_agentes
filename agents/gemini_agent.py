import google.generativeai as genai
import os

class GeminiAgent:
    def __init__(self, model_name="gemini-1.5-flash"):
        # Tenta GEMINI_API_KEY primeiro (nome no seu .env)
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        # Tenta configurar o genai. 
        # Se a API Key existir, usa ela. 
        # Se não, o SDK tentará encontrar credenciais ADC (CLI/Google Cloud) automaticamente.
        if api_key:
            genai.configure(api_key=api_key)
            print("Autenticado via API Key.")
        else:
            # Ao não passar api_key, o SDK busca o Application Default Credentials (ADC)
            # que é o que o 'gcloud auth application-default login' configura.
            try:
                genai.configure()
                print("Tentando autenticação via Google Cloud CLI (ADC)...")
            except Exception as e:
                print(f"Aviso: Não foi possível configurar autenticação automática: {e}")
        
        self.model = genai.GenerativeModel(model_name)
    
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
        print(agent.ask("Olá, quem é você?"))
    except Exception as e:
        print(e)
