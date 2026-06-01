import requests
import os
import time
from dotenv import load_dotenv

class SkyvernAgent:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("SKYVERN_API_KEY")
        self.base_url = "https://api.skyvern.com/v1"
        
        # Limite estimado: 5000 créditos mensais ~ 170 ações.
        self.is_cloud = True 

    def is_active(self):
        return self.api_key is not None and self.api_key != "seu_token_aqui"

    def run_task(self, url, prompt, max_steps=10):
        """
        Cria uma tarefa no Skyvern Cloud e aguarda a conclusão.
        """
        if not self.is_active():
            return "Erro: SKYVERN_API_KEY não configurada no .env."

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Payload corrigido conforme documentação v1
        payload = {
            "url": url,
            "prompt": prompt,
            "max_steps": max_steps,
            "proxy_location": "RESIDENTIAL" 
        }

        try:
            print(f"[Skyvern] Iniciando tarefa para {url}...")
            # 1. Criar a Tarefa
            response = requests.post(f"{self.base_url}/run/tasks", headers=headers, json=payload)
            
            if response.status_code != 201 and response.status_code != 200:
                return f"Erro na Skyvern API (Status {response.status_code}): {response.text}"
                
            task_data = response.json()
            # A API retorna run_id ou task_id dependendo da versão, tratamos ambos
            run_id = task_data.get("run_id") or task_data.get("task_id")
            
            if not run_id:
                return f"Erro: A API não retornou um ID de execução. Resposta: {task_data}"

            # 2. Loop de Polling (Aguardar conclusão)
            # Endpoint de polling: /v1/runs/{run_id} ou /v1/tasks/{run_id}
            max_retries = 30 
            for i in range(max_retries):
                time.sleep(10)
                # Tenta /runs primeiro (mais moderno)
                status_res = requests.get(f"{self.base_url}/runs/{run_id}", headers=headers)
                if status_res.status_code == 404:
                    # Tenta /tasks se falhar
                    status_res = requests.get(f"{self.base_url}/tasks/{run_id}", headers=headers)
                
                if status_res.status_code != 200:
                    print(f"[Skyvern] Aviso: Erro ao checar status (Status {status_res.status_code})")
                    continue

                status_data = status_res.json()
                status = status_data.get("status")
                
                print(f"[Skyvern] Status da execução {run_id}: {status} (Tentativa {i+1})")
                
                if status == "COMPLETED" or status == "SUCCESS":
                    return status_data.get("extracted_information") or status_data.get("result") or "Tarefa concluída com sucesso."
                elif status in ["FAILED", "TERMINATED", "ERROR"]:
                    return f"Erro: A tarefa Skyvern falhou com status {status}. Detalhes: {status_data.get('error_message')}"
            
            return f"Timeout: A tarefa {run_id} excedeu o tempo limite de espera."

        except Exception as e:
            return f"Erro ao interagir com Skyvern API: {str(e)}"

if __name__ == "__main__":
    agent = SkyvernAgent()
    if agent.is_active():
        print("Skyvern Agent Pronto!")
    else:
        print("Aguardando SKYVERN_API_KEY...")
