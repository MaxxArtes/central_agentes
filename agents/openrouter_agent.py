import requests
import json
import os

class OpenRouterAgent:
    def __init__(self, model_name="openrouter/free"):
        # Tenta api-key-openrouter primeiro
        self.api_key = os.getenv("api-key-openrouter") or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("Chave do OpenRouter não encontrada no .env")
        
        # O modelo padrão e mais estável recomendado é o free
        self.model_name = "openrouter/free" if "gemini" in model_name.lower() or model_name == "free" else model_name
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def ask(self, prompt, use_reasoning=True):
        """
        Envia uma requisição seguindo estritamente a documentação do OpenRouter.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/MaxxArtes/central_agentes",
            "X-Title": "Central de Agentes Carvalima",
        }
        
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        # Implementação exata do parâmetro de raciocínio da documentação
        if use_reasoning:
            data["reasoning"] = {"enabled": True}

        try:
            response = requests.post(url=self.url, headers=headers, data=json.dumps(data), timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # Extrai a mensagem da resposta
            message = result['choices'][0]['message']
            content = message.get('content', '')
            
            # Formata a resposta para incluir o raciocínio se estiver disponível
            # (conforme a doc: reasoning_details)
            reasoning_details = message.get('reasoning_details')
            if reasoning_details:
                return f"🤔 **Raciocínio:**\n{reasoning_details}\n\n---\n\n{content}"
            
            return content
            
        except Exception as e:
            # Fallback de segurança para openrouter/free
            if "404" in str(e) and self.model_name != "openrouter/free":
                self.model_name = "openrouter/free"
                return self.ask(prompt, use_reasoning)
            return f"Erro na API OpenRouter ({self.model_name}): {str(e)}"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    agent = OpenRouterAgent()
    print(f"Testando com: {agent.model_name}")
    print(agent.ask("Qual é a raiz quadrada de 144? Pense passo a passo."))
