from openai import OpenAI
import os

class OpenRouterAgent:
    def __init__(self, model_name="google/gemini-2.0-flash-001"):
        # Tenta api-key-openrouter primeiro (nome no seu .env)
        api_key = os.getenv("api-key-openrouter") or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("Chave do OpenRouter não encontrada no .env (procurei por 'api-key-openrouter')")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model_name = model_name
    
    def ask(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                extra_headers={
                    "HTTP-Referer": "https://github.com/MaxxArtes/central_agentes",
                    "X-Title": "Central de Agentes Carvalima",
                }
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro ao processar requisição no OpenRouter: {str(e)}"

if __name__ == "__main__":
    # Teste rápido
    from dotenv import load_dotenv
    load_dotenv()
    try:
        agent = OpenRouterAgent()
        print(agent.ask("Olá, qual modelo você é?"))
    except Exception as e:
        print(e)
