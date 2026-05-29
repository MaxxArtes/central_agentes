import os
import shutil
from pathlib import Path

class FileAgent:
    def __init__(self, base_dir=None):
        """
        Agente especializado em manipulação de arquivos e diretórios.
        Por padrão, opera na raiz do projeto.
        """
        self.base_dir = Path(base_dir or os.getcwd())

    def list_files(self, directory="."):
        """Lista arquivos em um diretório de forma estruturada."""
        try:
            target_path = self.base_dir / directory
            if not target_path.exists():
                return f"Erro: Diretório {directory} não encontrado."
            
            items = os.listdir(target_path)
            return {"directory": str(directory), "items": items}
        except Exception as e:
            return f"Erro ao listar arquivos: {str(e)}"

    def read_file(self, file_path):
        """Lê o conteúdo de um arquivo."""
        try:
            target_file = self.base_dir / file_path
            if not target_file.is_file():
                return f"Erro: {file_path} não é um arquivo válido."
            
            with open(target_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"

    def write_file(self, file_path, content):
        """Cria ou sobrescreve um arquivo com o conteúdo fornecido."""
        try:
            target_file = self.base_dir / file_path
            # Cria pastas pai se não existirem
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Arquivo {file_path} salvo com sucesso."
        except Exception as e:
            return f"Erro ao escrever arquivo: {str(e)}"

    def delete_file(self, file_path):
        """Remove um arquivo de forma definitiva."""
        try:
            target_file = self.base_dir / file_path
            if target_file.exists():
                os.remove(target_file)
                return f"Arquivo {file_path} deletado."
            return "Arquivo não encontrado."
        except Exception as e:
            return f"Erro ao deletar: {str(e)}"

if __name__ == "__main__":
    agent = FileAgent()
    print("Teste FileAgent:")
    print(agent.list_files())
