import os
from agents.gemini_agent import GeminiAgent
from agents.openrouter_agent import OpenRouterAgent
from agents.groq_agent import GroqAgent
from agents.gemini_cli_agent import GeminiCliAgent
from agents.huggingface_agent import HuggingFaceAgent
from agents.github_agent import GitHubAgent
from agents.file_agent import FileAgent
from agents.ide_agent import IDEAgent
from agents.docker_agent import DockerAgent
from agents.search_agent import SearchAgent
from agents.google_agent import GoogleAgent
from agents.discord_agent import DiscordAgent
from agents.expansion_agents import NotionAgent, TelegramAgent, SlackAgent
from agents.colab_agent import ColabAgent
from agents.database_agent import DatabaseAgent
from tools.scraper import SimpleScraper
from tools.browser_manager import AutonomousBrowser
from utils.context_manager import ContextManager
import asyncio
import json

class CentralOrchestrator:
    def __init__(self):
        # Gerenciador de Memória Compartilhada
        self.memory = ContextManager()
        
        # O Maestro agora é o Gemini Nativo via CLI
        self.brain = GeminiCliAgent()
        
        # Ferramentas auxiliares
        self.browser = AutonomousBrowser(model_name="openrouter/free")
        
        # Agentes especializados
        self.hf_agent = HuggingFaceAgent()
        self.github_agent = GitHubAgent()
        self.file_agent = FileAgent()
        self.ide_agent = IDEAgent()
        self.docker_agent = DockerAgent()
        self.search_agent = SearchAgent()
        self.google_agent = GoogleAgent()
        self.discord_agent = DiscordAgent()
        self.notion_agent = NotionAgent()
        self.telegram_agent = TelegramAgent()
        self.slack_agent = SlackAgent()
        self.colab_agent = ColabAgent()
        self.db_agent = DatabaseAgent() # Especialista em Banco de Dados
        
        try:
            self.fast_agent = GroqAgent()
        except:
            self.fast_agent = None
    
    def decide_and_execute(self, user_input):
        # Recupera o contexto histórico para o cérebro
        history_context = self.memory.get_context_summary()
        
        system_prompt = f"""
        Você é o Orquestrador da Central de Agentes Carvalima.
        Sua missão é triar o pedido do usuário e decidir qual ferramenta deve ser ativada.
        
        {history_context}
        
        REGRAS OBRIGATÓRIAS:
        1. RESPONDA APENAS UM JSON PURO. NADA DE TEXTO ANTES OU DEPOIS.
        2. O JSON DEVE TER EXATAMENTE ESTAS CHAVES: "decision", "reason", "instructions".
        
        VALORES PARA "decision":
        - "database": Use para salvar dados permanentemente, fazer buscas em logs antigos ou executar SQL.
        - "quick_search": Busca rápida.
        - "browser": Navegação complexa.
        - "colab": Notebooks Google.
        - "notion": Notas e wikis.
        - "telegram/slack/discord": Comunicação.
        - "google_workspace": Drive/Docs.
        - "github": GitHub tasks.
        - "filesystem": Arquivos locais.
        - "ide_control": VS Code.
        - "docker": Containers.
        - "deep_chat": Análise complexa.
        """
        
        # Adiciona a entrada do usuário à memória volátil
        self.memory.add_interaction("user", user_input)
        
        # Se o banco estiver ativo, salva permanentemente
        if self.db_agent.is_active():
            self.db_agent.save_interaction("user", user_input)
        
        analysis_prompt = f"{system_prompt}\n\nPedido do usuário: {user_input}"
        
        # O cérebro decide usando o CLI com consciência do histórico
        decision_json_raw = self.brain.ask(analysis_prompt)
        
        # Limpa formatação Markdown do JSON
        decision_json_raw = decision_json_raw.replace("```json", "").replace("```", "").strip()
        
        try:
            # Tenta decodificar a decisão do cérebro principal
            decision = json.loads(decision_json_raw)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON do cérebro principal (Gemini CLI): {e}. Acionando fallback para o cérebro rápido (Groq).")
            # Se o cérebro principal falhar (ex: limite de taxa), usa o Groq como fallback para tomar a decisão
            try:
                if not self.fast_agent:
                    raise ValueError("Agente rápido (Groq) não está disponível para fallback.")
                decision_json_raw = self.fast_agent.ask(analysis_prompt)
                decision_json_raw = decision_json_raw.replace("```json", "").replace("```", "").strip()
                decision = json.loads(decision_json_raw)
            except Exception as fallback_e:
                # Se até o fallback falhar, recorre ao modo chat simples
                return self._fallback_to_chat(history_context, user_input, str(fallback_e))

        try:
            result = ""
            if decision["decision"] == "database" and self.db_agent.is_active():
                # NOTA: O DatabaseAgent atual só suporta 'save_interaction'. A decisão de "executar query" do LLM será salva como um log.
                result = f"🗄️ **Banco de Dados (Log):**\n\n" + self.db_agent.save_interaction("log", decision["instructions"])

            elif decision["decision"] == "colab":
                result = f"🧪 **Google Colab:**\n\n" + self.colab_agent.create_notebook("Notebook_Analise", decision["instructions"])

            elif decision["decision"] == "notion":
                result = f"📔 **Notion:**\n\n" + self.notion_agent.create_page("ID_DA_PAGINA_PAI", decision["instructions"])
            
            elif decision["decision"] == "telegram":
                result = f"✈️ **Telegram:**\n\n" + self.telegram_agent.send_message(decision["instructions"])
                
            elif decision["decision"] == "slack":
                result = f"🐝 **Slack:**\n\n" + self.slack_agent.post_message("#geral", decision["instructions"])

            elif decision["decision"] == "docker":
                instr = decision["instructions"].lower()
                if "liste" in instr or "list" in instr:
                    result = f"🐳 **Docker Status:**\n\n" + str(self.docker_agent.list_containers())
                else:
                    result = "Comando Docker reconhecido, mas o Docker Desktop pode estar desligado."

            elif decision["decision"] == "ide_control":
                instr = decision["instructions"].lower()
                if "abra" in instr or "open" in instr:
                    target = decision["instructions"].split("'")[1] if "'" in decision["instructions"] else decision["instructions"].split()[-1]
                    result = f"🖥️ **IDE Control:**\n\n" + self.ide_agent.open_in_code(target)
                elif "instale" in instr or "install" in instr:
                    ext_id = decision["instructions"].split()[-1]
                    result = f"📦 **IDE Setup:**\n\n" + self.ide_agent.install_extension(ext_id)
                else:
                    result = "Comando de IDE não reconhecido."

            elif decision["decision"] == "filesystem":
                instr = decision["instructions"].lower()
                if "leia" in instr or "read" in instr:
                    filename = decision["instructions"].split("'")[1] if "'" in decision["instructions"] else decision["instructions"].split()[-1]
                    result = f"📄 **Conteúdo do Arquivo ({filename}):**\n\n" + self.file_agent.read_file(filename)
                elif "liste" in instr or "list" in instr:
                    res = self.file_agent.list_files()
                    result = f"📁 **Arquivos no diretório:**\n\n" + ", ".join(res["items"]) if isinstance(res, dict) else res
                elif "crie" in instr or "escreva" in instr or "write" in instr:
                    result = f"💾 **Status do Filesystem:**\n\n" + self.file_agent.write_file("novo_arquivo.txt", "Conteúdo gerado via Orquestrador.")
                else:
                    result = "Tarefa de sistema de arquivos não reconhecida."

            elif decision["decision"] == "github" and self.github_agent.is_active():
                # Lógica de GitHub
                instr = decision["instructions"].lower()
                if "crie um repositório" in instr or "create repo" in instr:
                    name = user_input.split()[-1].replace("'","").replace('"',"")
                    result = f"🛠️ **GitHub (API):**\n\n" + self.github_agent.create_repo(name, description="Criado via Agente Gemini")
                elif "liste" in instr or "list" in instr:
                    result = f"📂 **Seus Repositórios:**\n\n" + "\n".join(self.github_agent.list_my_repos())
                else:
                    result = "Comando GitHub reconhecido, mas ação não mapeada."

            elif decision["decision"] == "nlp_specialist":
                if "traduz" in user_input.lower() or "traduza" in user_input.lower():
                    result = f"🌍 **Tradução Especializada (HF):**\n\n" + self.hf_agent.translate(user_input)
                else:
                    result = f"🤖 **Análise Hugging Face:**\n\n" + self.hf_agent.ask(decision["instructions"])

            elif decision["decision"] == "fast_chat" and self.fast_agent:
                result = f"⚡ **Resposta Rápida (Groq):**\n\n" + self.fast_agent.ask(user_input)
                
            else:
                # Para deep_chat ou fallback
                result = self.brain.ask(f"{history_context}\n\nUsuário: {user_input}")

            # Salva o resultado na memória para a próxima iteração
            self.memory.add_interaction("assistant", str(result))
            return result

        except Exception as e:
            return self._fallback_to_chat(history_context, user_input, str(e))

    def _fallback_to_chat(self, history_context, user_input, error_msg):
        """Fallback final para modo chat quando todas as outras lógicas falham."""
        print(f"ERRO CRÍTICO NO ORQUESTRADOR: {error_msg}. Recorrendo ao modo chat.")
        fallback_res = self.brain.ask(f"{history_context}\n\nUsuário: {user_input}")
        self.memory.add_interaction("assistant", fallback_res)
        return fallback_res

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    orch = CentralOrchestrator()
    print(orch.decide_and_execute("Vá ao site do Google e pesquise o valor do dólar agora."))
