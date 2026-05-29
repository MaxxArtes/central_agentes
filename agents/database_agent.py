from supabase import create_client, Client
import os
from dotenv import load_dotenv

class DatabaseAgent:
    def __init__(self):
        """
        Agente de Banco de Dados via API do Supabase.
        Mais fácil de configurar que o PostgreSQL puro.
        """
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        self.supabase = None
        if url and key:
            try:
                self.supabase = create_client(url, key)
                print("[Database] Conectado ao Supabase via API.")
            except Exception as e:
                print(f"[Database] Erro ao conectar: {e}")

    def is_active(self):
        return self.supabase is not None

    def save_interaction(self, role, content):
        """Salva uma interação em uma tabela 'memory' no Supabase."""
        if not self.is_active(): return "Supabase não configurado."
        try:
            data = {"role": role, "content": content}
            self.supabase.table("memory").insert(data).execute()
            return "Interação salva no Supabase."
        except Exception as e:
            return f"Erro ao salvar: {str(e)}"

if __name__ == "__main__":
    agent = DatabaseAgent()
    if agent.is_active():
        print("Conexão OK!")
    else:
        print("Aguardando SUPABASE_URL e SUPABASE_KEY no .env")
