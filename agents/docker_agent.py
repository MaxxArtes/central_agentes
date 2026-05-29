import docker
import os

class DockerAgent:
    def __init__(self):
        """
        Agente especializado em gerenciar containers Docker.
        """
        try:
            self.client = docker.from_env()
        except Exception:
            self.client = None

    def is_active(self):
        if not self.client:
            return False
        try:
            self.client.ping()
            return True
        except:
            return False

    def list_containers(self, all=False):
        """Lista os containers no sistema."""
        if not self.is_active():
            return "Erro: Docker Desktop não está rodando ou não está acessível."
        try:
            containers = self.client.containers.list(all=all)
            if not containers:
                return "Nenhum container encontrado."
            return [f"{c.name} ({c.status})" for c in containers]
        except Exception as e:
            return f"Erro ao listar containers: {str(e)}"

    def run_container(self, image, name=None, detach=True, ports=None):
        """Inicia um novo container."""
        if not self.is_active():
            return "Erro: Docker não está ativo."
        try:
            container = self.client.containers.run(
                image, 
                name=name, 
                detach=detach, 
                ports=ports
            )
            return f"Container '{container.name}' iniciado com sucesso."
        except Exception as e:
            return f"Erro ao iniciar container: {str(e)}"

if __name__ == "__main__":
    agent = DockerAgent()
    if agent.is_active():
        print("Docker detectado e ativo!")
        print(agent.list_containers())
    else:
        print("Docker SDK instalada, mas o serviço não está rodando no momento.")
