import google.generativeai as genai
import os

class GeminiAgent:
    def __init__(self, model_name="gemini-1.5-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
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
