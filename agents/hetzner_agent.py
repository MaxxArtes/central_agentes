from hcloud import Client
from hcloud.servers.domain import Server
import os
from dotenv import load_dotenv

class HetznerAgent:
    def __init__(self):
        """
        Agente para gerenciamento de infraestrutura na Hetzner Cloud.
        Permite listar servidores, verificar status e gerenciar recursos.
        """
        load_dotenv()
        self.api_token = os.getenv("HETZNER_API_TOKEN")
        self.client = None
        if self.api_token:
            try:
                self.client = Client(token=self.api_token)
            except Exception as e:
                print(f"[Hetzner] Erro ao inicializar cliente: {e}")

    def is_active(self):
        return self.client is not None

    def list_servers(self):
        """Lista todos os servidores na conta Hetzner Cloud."""
        if not self.is_active(): return "Erro: HETZNER_API_TOKEN não configurado."
        try:
            servers = self.client.servers.get_all()
            result = []
            for s in servers:
                result.append({
                    "id": s.id,
                    "name": s.name,
                    "status": s.status,
                    "ip": s.public_net.ipv4.ip,
                    "location": s.datacenter.location.name
                })
            return result
        except Exception as e:
            return f"Erro ao listar servidores: {str(e)}"

    def get_server_info(self, server_name):
        """Busca informações detalhadas de um servidor específico por nome."""
        if not self.is_active(): return "HETZNER_API_TOKEN não configurado."
        try:
            server = self.client.servers.get_by_name(server_name)
            if not server: return f"Servidor '{server_name}' não encontrado."
            return {
                "name": server.name,
                "status": server.status,
                "cores": server.server_type.cores,
                "memory": server.server_type.memory,
                "disk": server.server_type.disk,
                "traffic_limit": server.included_traffic
            }
        except Exception as e:
            return f"Erro ao buscar servidor: {str(e)}"

    def reboot_server(self, server_name):
        """Reinicia um servidor por nome."""
        if not self.is_active(): return "HETZNER_API_TOKEN não configurado."
        try:
            server = self.client.servers.get_by_name(server_name)
            if not server: return f"Servidor '{server_name}' não encontrado."
            server.reboot()
            return f"Comando de reinicialização enviado para '{server_name}'."
        except Exception as e:
            return f"Erro ao reiniciar: {str(e)}"

if __name__ == "__main__":
    agent = HetznerAgent()
    if agent.is_active():
        print("Hetzner Agent Ativo!")
        print(agent.list_servers())
    else:
        print("Aguardando HETZNER_API_TOKEN no .env")
