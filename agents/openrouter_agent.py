from openai import OpenAI
import os
import json

class OpenRouterAgent:
    # Mapeamento centralizado de modelos
    MODEL_MAP = {
        "gemini-1.5-flash": "google/gemini-2.0-flash-001",
        "gemini-1.5-pro": "google/gemini-pro-1.5-exp",
        "free": "openrouter/free",
        "auto": "openrouter/free"
    }

    def __init__(self, model_name="openrouter/free"):
        # Tenta api-key-openrouter primeiro (nome no seu .env)
        api_key = os.getenv("api-key-openrouter") or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("Chave do OpenRouter não encontrada no .env")
        
        # Resolve o ID real do modelo
        self.model_name = self.MODEL_MAP.get(model_name, model_name)
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    
    def ask(self, prompt, use_reasoning=True):
        try:
            # Prepara os parâmetros da requisição conforme a nova doc fornecida
            # O OpenRouter aceita parâmetros extras no corpo via extra_body
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "extra_headers": {
                    "HTTP-Referer": "https://github.com/MaxxArtes/central_agentes",
                    "X-Title": "Central de Agentes Carvalima",
                }
            }
            
            # Ativa o raciocínio se solicitado (Chain of Thought)
            if use_reasoning:
                payload["extra_body"] = {"reasoning": {"enabled": True}}

            response = self.client.chat.completions.create(**payload)
            
            # Retorna o conteúdo da resposta
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro no OpenRouter ({self.model_name}): {str(e)}"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    # Testando com o modelo gratuito e raciocínio ativado
    agent = OpenRouterAgent(model_name="free")
    print(f"--- Testando OpenRouter Free com Raciocínio ---")
    print(f"Modelo: {agent.model_name}")
    print(agent.ask("Quanto é 25 * 14? Explique o passo a passo."))
