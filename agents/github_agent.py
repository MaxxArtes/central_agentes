from github import Github
import os
from dotenv import load_dotenv

class GitHubAgent:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("GITHUB_ACCESS_TOKEN")
        if not self.token or self.token == "seu_token_aqui":
            self.gh = None
            print("[GitHub] Aviso: GITHUB_ACCESS_TOKEN não configurado no .env")
        else:
            self.gh = Github(self.token)

    def is_active(self):
        return self.gh is not None

    def list_my_repos(self):
        if not self.is_active(): return "GitHub não configurado."
        try:
            repos = self.gh.get_user().get_repos()
            return [repo.full_name for repo in repos[:10]] # Retorna os 10 primeiros
        except Exception as e:
            return f"Erro ao listar repos: {str(e)}"

    def create_repo(self, name, description="", private=True):
        if not self.is_active(): return "GitHub não configurado."
        try:
            user = self.gh.get_user()
            repo = user.create_repo(name, description=description, private=private)
            return f"Repositório criado com sucesso: {repo.html_url}"
        except Exception as e:
            return f"Erro ao criar repo: {str(e)}"

    def create_issue(self, repo_name, title, body=""):
        if not self.is_active(): return "GitHub não configurado."
        try:
            repo = self.gh.get_repo(repo_name)
            issue = repo.create_issue(title=title, body=body)
            return f"Issue #{issue.number} criada em {repo_name}"
        except Exception as e:
            return f"Erro ao criar issue: {str(e)}"

if __name__ == "__main__":
    agent = GitHubAgent()
    if agent.is_active():
        print("Conectado ao GitHub!")
        print("Seus repositórios:", agent.list_my_repos())
    else:
        print("Aguardando configuração do token no .env...")
