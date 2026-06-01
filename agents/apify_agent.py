import requests
import os
import json
from dotenv import load_dotenv

class ApifyAgent:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv("APIFY_API_TOKEN")
        self.base_url = "https://api.apify.com/v2"
        
        # Limite de segurança: não rodar se o crédito estiver abaixo de $0.10
        self.safety_buffer = 0.10 

    def is_active(self):
        return self.api_token is not None and self.api_token != "seu_token_aqui"

    def get_remaining_credits(self):
        """
        Consulta o saldo remanescente na conta Apify.
        Nota: A API do Apify retorna informações sobre o uso do plano.
        """
        if not self.is_active(): return 0
        
        url = f"{self.base_url}/users/me"
        params = {"token": self.api_token}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get("data", {})
            
            # O Apify trabalha com 'monthlyUsageUsd'. 
            # Subtraímos o uso do limite de $5.00
            usage = data.get("subscription", {}).get("monthlyUsageUsd", 0)
            limit = 5.00 # Plano Free
            remaining = max(0, limit - usage)
            return round(remaining, 2)
        except Exception as e:
            print(f"[Apify] Erro ao checar créditos: {e}")
            return 0

    def run_actor(self, actor_id, input_data):
        """
        Executa um Actor específico e aguarda o resultado.
        """
        if not self.is_active():
            return "Erro: APIFY_API_TOKEN não configurado."
        
        if not actor_id:
            return "Erro: ID do Actor não fornecido."
        
        # Correção automática de formato se necessário (troca / por ~)
        actor_id = actor_id.replace("/", "~")
        
        credits = self.get_remaining_credits()
        if credits < self.safety_buffer:
            return f"Erro: Créditos Apify insuficientes (${credits}). Operação cancelada para poupar recursos."

        print(f"[Apify] Créditos disponíveis: ${credits}. Iniciando Actor {actor_id}...")
        
        # Endpoint síncrono para obter itens diretamente: 
        # POST /v2/acts/{actorId}/run-sync-get-dataset-items?token=...
        url = f"{self.base_url}/acts/{actor_id}/run-sync-get-dataset-items"
        params = {"token": self.api_token, "timeout": 60}
        
        try:
            # Esta chamada espera o Actor terminar (até o timeout) e retorna os itens do dataset
            response = requests.post(url, params=params, json=input_data, timeout=120)
            
            if response.status_code == 201 or response.status_code == 200:
                return response.json()
            else:
                # Se falhar o síncrono, tenta o assíncrono básico
                fallback_url = f"{self.base_url}/acts/{actor_id}/runs"
                res = requests.post(fallback_url, params={"token": self.api_token}, json=input_data)
                if res.status_code == 201:
                    return f"O Actor {actor_id} iniciou em modo assíncrono (ID: {res.json()['data']['id']}). Os resultados estarão disponíveis no console do Apify em breve."
                return f"Erro no Apify (Status {response.status_code}): {response.text}"

        except requests.exceptions.Timeout:
            return "Erro: A execução do Actor no Apify demorou muito (Timeout). Verifique o progresso no painel do Apify."
        except Exception as e:
            return f"Erro ao executar Actor no Apify: {str(e)}"

if __name__ == "__main__":
    agent = ApifyAgent()
    print(f"Créditos Apify: ${agent.get_remaining_credits()}")
