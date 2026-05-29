from openai import OpenAI
import os

class OpenRouterAgent:
    # Mapeamento centralizado de modelos para garantir que IDs antigos não causem 404
    # Usando modelos Versão 2 que são os mais estáveis no OpenRouter atualmente
    MODEL_MAP = {
        "gemini-1.5-flash": "google/gemini-2.0-flash-001",
        "gemini-1.5-pro": "google/gemini-2.0-flash-001", # Fallback para Flash 2.0 se Pro 1.5 der 404
        "google/gemini-1.5-flash": "google/gemini-2.0-flash-001",
        "google/gemini-1.5-pro": "google/gemini-2.0-flash-001",
        "google/gemini-pro-1.5": "google/gemini-2.0-flash-001",
        "google/gemini-pro-1.5-exp": "google/gemini-2.0-flash-001"
    }

    def __init__(self, model_name="google/gemini-2.0-flash-001"):
        # Tenta api-key-openrouter primeiro (nome no seu .env)
        api_key = os.getenv("api-key-openrouter") or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("Chave do OpenRouter não encontrada no .env (procurei por 'api-key-openrouter')")
        
        # Resolve o ID real do modelo no OpenRouter
        self.model_name = self.MODEL_MAP.get(model_name, model_name)
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    
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
            # Tenta um último fallback para o modelo mais básico se o mapeado falhar
            if "404" in str(e) and self.model_name != "google/gemini-2.0-flash-001":
                try:
                    response = self.client.chat.completions.create(
                        model="google/gemini-2.0-flash-001",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return response.choices[0].message.content
                except:
                    pass
            return f"Erro ao processar requisição no OpenRouter ({self.model_name}): {str(e)}"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    try:
        agent = OpenRouterAgent(model_name="gemini-1.5-pro")
        print(f"Testando com: {agent.model_name}")
        print(agent.ask("Diga 'Funciona!'"))
    except Exception as e:
        print(e)
