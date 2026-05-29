import subprocess
import os

class IDEAgent:
    def __init__(self):
        """
        Agente especializado em interagir com o VS Code via CLI.
        """
        pass

    def open_in_code(self, path="."):
        """Abre um arquivo ou diretório no VS Code."""
        try:
            # Verifica se o caminho existe antes de tentar abrir
            if not os.path.exists(path):
                return f"Erro: O caminho '{path}' não existe."
            
            # Executa o comando 'code' de forma não bloqueante
            subprocess.Popen(['code', path], shell=True)
            return f"Sucesso: Abrindo '{path}' no VS Code."
        except Exception as e:
            return f"Erro ao interagir com o VS Code: {str(e)}"

    def install_extension(self, extension_id):
        """Instala uma extensão no VS Code pelo ID (ex: ms-python.python)."""
        try:
            result = subprocess.run(['code', '--install-extension', extension_id], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return f"Extensão '{extension_id}' instalada com sucesso."
            else:
                return f"Erro ao instalar extensão: {result.stderr}"
        except Exception as e:
            return f"Erro: {str(e)}"

if __name__ == "__main__":
    agent = IDEAgent()
    print("Teste IDEAgent (Apenas informativo, não abre nada agora):")
    # print(agent.open_in_code(".")) # Teste real abriria a pasta atual
