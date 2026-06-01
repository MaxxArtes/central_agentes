import requests
import os
from dotenv import load_dotenv

class Base44Agent:
    def __init__(self):
        """
        Agente para integração com a plataforma Base44.com (AI App Builder).
        Permite que a central interaja com aplicativos e fluxos criados no Base44.
        """
        load_dotenv()
        self.api_key = os.getenv("base44_api") or os.getenv("BASE44_API_KEY")
        self.base_url = "https://api.base44.com/v1"

    def is_active(self):
        return self.api_key is not None and self.api_key != "seu_token_aqui" and len(self.api_key) > 5

    def call_integration(self, integration_id, action, params):
        """
        Chama uma integração configurada no Base44.
        Ex: Usar um conector de logística que já está pronto lá.
        """
        if not self.is_active(): return "Erro: BASE44_API_KEY não configurada."
        
        url = f"{self.base_url}/integrations/{integration_id}/call"
        headers = {"x-api-key": self.api_key}
        data = {
            "action": action,
            "params": params
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Erro ao chamar integração Base44: {str(e)}"

    def get_entity(self, entity_name, record_id=None):
        """
        Recupera dados de uma 'Entity' (Tabela/Banco de Dados) do Base44.
        """
        if not self.is_active(): return "Erro: BASE44_API_KEY não configurada."
        
        url = f"{self.base_url}/entities/{entity_name}"
        if record_id:
            url += f"/{record_id}"
            
        headers = {"x-api-key": self.api_key}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Erro ao buscar entidade Base44: {str(e)}"

    def create_record(self, entity_name, data):
        """
        Cria um novo registro em uma entidade do Base44.
        """
        if not self.is_active(): return "Erro: BASE44_API_KEY não configurada."
        
        url = f"{self.base_url}/entities/{entity_name}"
        headers = {"x-api-key": self.api_key}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return f"Registro criado com sucesso na entidade '{entity_name}'."
        except Exception as e:
            return f"Erro ao criar registro no Base44: {str(e)}"

if __name__ == "__main__":
    agent = Base44Agent()
    if agent.is_active():
        print("Base44 Agent Conectado!")
    else:
        print("Aguardando BASE44_API_KEY no .env")
