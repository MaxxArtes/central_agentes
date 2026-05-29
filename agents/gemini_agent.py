import google.generativeai as genai
import os

class GeminiAgent:
    def __init__(self, model_name="gemini-1.5-flash"):
        # PRIORIDADE 1: Tentar autenticação via Google Cloud CLI (ADC)
        # Isso garante que usemos os limites altos da sua conta logada.
        try:
            # Se você rodou 'gcloud auth application-default login', 
            # o configure() sem argumentos vai encontrar as credenciais.
            genai.configure()
            print(f"[{model_name}] Tentando autenticação via Google Cloud CLI (ADC)...")
        except Exception:
            # PRIORIDADE 2: Fallback para API Key se a CLI não estiver configurada
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                print(f"[{model_name}] CLI não encontrada. Usando API Key do .env.")
            else:
                print(f"[{model_name}] Aviso: Nenhuma forma de autenticação encontrada.")
        
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
