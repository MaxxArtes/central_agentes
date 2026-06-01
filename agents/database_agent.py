from supabase import create_client, Client
import os
from dotenv import load_dotenv

class DatabaseAgent:
    def __init__(self):
        """
        Agente de Banco de Dados via API do Supabase.
        Evoluído para suportar Memória de Longo Prazo e Logs Estruturados.
        """
        load_dotenv()
        url = os.getenv("suapbase_api_url") or os.getenv("SUPABASE_URL")
        key = os.getenv("suapbase_anon_public_key") or os.getenv("SUPABASE_KEY")
        
        self.supabase = None
        if url and key:
            try:
                self.supabase = create_client(url, key)
                print("[Database] Conectado ao Supabase via API.")
            except Exception as e:
                print(f"[Database] Erro ao conectar: {e}")

    def is_active(self):
        return self.supabase is not None

    def save_interaction(self, role, content, task_id=None, metadata=None):
        """
        Salva uma interação com suporte a metadados e IDs de tarefa.
        """
        if not self.is_active(): return "Supabase não configurado."
        try:
            data = {
                "role": role, 
                "content": content,
                "task_id": task_id,
                "metadata": metadata or {}
            }
            # Tenta inserir na tabela 'memory'. Se colunas novas não existirem, o Supabase ignora ou erro.
            # Recomendação: Adicionar task_id (text) e metadata (jsonb) no painel do Supabase.
            self.supabase.table("memory").insert(data).execute()
            return "✅ Interação persistida na memória de longo prazo."
        except Exception as e:
            # Fallback para colunas básicas se a tabela não tiver sido atualizada
            try:
                basic_data = {"role": role, "content": content}
                self.supabase.table("memory").insert(basic_data).execute()
                return "✅ Interação salva (modo básico)."
            except:
                return f"❌ Erro ao salvar no Supabase: {str(e)}"

    def get_recent_context(self, limit=15):
        """Recupera o histórico mais recente para fornecer contexto ao Orquestrador."""
        if not self.is_active(): return ""
        try:
            response = self.supabase.table("memory")\
                .select("role, content")\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            history = response.data[::-1] # Inverte para ordem cronológica
            context = "--- MEMÓRIA DE LONGO PRAZO (HISTÓRICO RECENTE) ---\n"
            for entry in history:
                context += f"{entry['role'].upper()}: {entry['content'][:300]}\n"
            return context
        except Exception as e:
            return f"Erro ao buscar memória: {e}"

    def search_memory(self, query):
        """Busca palavras-chave no histórico passado."""
        if not self.is_active(): return "Memória inativa."
        try:
            response = self.supabase.table("memory")\
                .select("*")\
                .ilike("content", f"%{query}%")\
                .limit(5)\
                .execute()
            return response.data
        except Exception as e:
            return f"Erro na busca de memória: {e}"

if __name__ == "__main__":
    agent = DatabaseAgent()
    if agent.is_active():
        print("Teste de busca de memória para 'Oscar':")
        print(agent.search_memory("Oscar"))
    else:
        print("Aguardando chaves no .env")
