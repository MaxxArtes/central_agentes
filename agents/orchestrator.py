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
from agents.apify_agent import ApifyAgent
from agents.skyvern_agent import SkyvernAgent
from agents.base44_agent import Base44Agent
from tools.scraper import SimpleScraper
from tools.browser_manager import AutonomousBrowser
from utils.context_manager import ContextManager
import asyncio
import json

class CentralOrchestrator:
    def __init__(self):
        # Gerenciador de Memória Compartilhada (Volátil)
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
        self.db_agent = DatabaseAgent() 
        self.apify_agent = ApifyAgent()
        self.skyvern_agent = SkyvernAgent()
        self.base44_agent = Base44Agent()
        
        try:
            self.fast_agent = GroqAgent()
        except:
            self.fast_agent = None
    
    def decide_and_execute(self, user_input, max_steps=10):
        """
        Executa um loop autônomo de Raciocínio -> Ação -> Observação.
        Utiliza memória de longo prazo (Supabase) para contexto histórico.
        """
        # Recupera o contexto da memória de longo prazo (Supabase) + histórico recente
        long_term_history = self.db_agent.get_recent_context(limit=10)
        execution_log = []
        
        # Monitoramento de recursos
        apify_credits = self.apify_agent.get_remaining_credits()
        skyvern_active = self.skyvern_agent.is_active()
        base44_active = self.base44_agent.is_active()
        
        for step in range(1, max_steps + 1):
            steps_taken = "\n".join([f"Passo {i}: {log}" for i, log in enumerate(execution_log, 1)])
            
            system_prompt = f"""
            Você é o Cérebro do Orquestrador Autônomo (Modo Manus).
            Objetivo Final: {user_input}
            
            {long_term_history}
            
            PROGRESSO DA TAREFA ATUAL:
            {steps_taken if steps_taken else "Iniciando tarefa agora."}
            
            RECURSOS DISPONÍVEIS:
            - Apify Credits: ${apify_credits} (Extração massiva)
            - Skyvern Status: {"Ativo" if skyvern_active else "Inativo"} (Navegação visual complexa)
            - Base44 Status: {"Ativo" if base44_active else "Inativo"} (App de IA/Logística)
            - Local Browser: Grátis (Navegação rápida)
            
            INSTRUÇÕES:
            1. Analise o progresso e decida a PRÓXIMA MELHOR AÇÃO.
            2. Se uma ferramenta falhar, TENTE OUTRA estratégia.
            3. Responda APENAS um JSON puro com: "decision", "reason", "instructions".
            
            DECISÕES POSSÍVEIS:
            - "finish": {{"instructions": "Resposta final detalhada"}}
            - "browser": {{"instructions": "Tarefa para o navegador local"}}
            - "skyvern": {{"url": "URL", "prompt": "Instrução visual"}}
            - "apify": {{"actor_id": "ID", "input": {{"key": "value"}}}}
            - "base44_call": {{"integration_id": "ID", "action": "ação", "params": {{}}}}
            - "base44_data": {{"entity": "nome", "action": "get|create", "record_id": "opcional", "data": {{}}}}
            - "quick_search": {{"instructions": "Busca"}}
            - "file_write": {{"instructions": {{"path": "nome.txt", "content": "conteúdo"}}}}
            - "database_search": {{"query": "termo"}} - Use para buscar em memórias antigas no Supabase.
            """
            
            decision_json_raw = self.brain.ask(system_prompt)
            decision_json_raw = decision_json_raw.replace("```json", "").replace("```", "").strip()
            
            try:
                decision = json.loads(decision_json_raw)
            except Exception as e:
                if self.fast_agent:
                    decision_json_raw = self.fast_agent.ask(system_prompt)
                    decision_json_raw = decision_json_raw.replace("```json", "").replace("```", "").strip()
                    try:
                        decision = json.loads(decision_json_raw)
                    except:
                        return self._fallback_to_chat(long_term_history, user_input, "Falha no JSON.")
                else:
                    return self._fallback_to_chat(long_term_history, user_input, str(e))

            print(f"[PASSO {step}] {decision['decision']}: {decision['reason']}")
            
            try:
                result = ""
                d_type = decision["decision"]
                instr = decision.get("instructions", {})

                if d_type == "finish":
                    final_res = instr
                    # Persistência final na Memória de Longo Prazo e Volátil
                    self.db_agent.save_interaction("user", user_input)
                    self.db_agent.save_interaction("assistant", final_res)
                    self.memory.add_interaction("user", user_input)
                    self.memory.add_interaction("assistant", final_res)
                    return final_res

                elif d_type == "database_search":
                    result = str(self.db_agent.search_memory(decision.get("query", "")))

                elif d_type == "base44_call":
                    result = self.base44_agent.call_integration(
                        decision.get("integration_id"),
                        decision.get("action"),
                        decision.get("params", {})
                    )

                elif d_type == "base44_data":
                    entity = decision.get("entity")
                    action = decision.get("action", "get")
                    if action == "get":
                        result = self.base44_agent.get_entity(entity, decision.get("record_id"))
                    else:
                        result = self.base44_agent.create_record(entity, decision.get("data", {}))

                elif d_type == "skyvern":
                    url = decision.get("url")
                    prompt = decision.get("prompt")
                    result = self.skyvern_agent.run_task(url, prompt)

                elif d_type == "apify":
                    actor_id = decision.get("actor_id")
                    actor_input = decision.get("input", {})
                    result = self.apify_agent.run_actor(actor_id, actor_input)
                    apify_credits = self.apify_agent.get_remaining_credits()

                elif d_type == "browser":
                    result = asyncio.run(self.browser.run_task(instr))

                elif d_type == "quick_search":
                    result = self.search_agent.quick_search(instr)

                elif d_type == "file_write":
                    path = instr.get("path", "output.txt") if isinstance(instr, dict) else "output.txt"
                    content = instr.get("content", "") if isinstance(instr, dict) else str(instr)
                    result = self.file_agent.write_file(path, content)

                elif d_type == "file_read":
                    result = self.file_agent.read_file(instr)

                elif d_type == "file_list":
                    result = str(self.file_agent.list_files(instr))

                elif d_type == "github_create_repo":
                    result = self.github_agent.create_repo(instr)

                elif d_type == "github_list_repos":
                    result = str(self.github_agent.list_my_repos())

                elif d_type == "messenger":
                    plat = instr.get("platform", "telegram").lower() if isinstance(instr, dict) else "telegram"
                    msg = instr.get("message", "") if isinstance(instr, dict) else str(instr)
                    if plat == "telegram": result = self.telegram_agent.send_message(msg)
                    elif plat == "slack": result = self.slack_agent.post_message("#geral", msg)
                    elif plat == "discord": result = self.discord_agent.send_message(msg)

                elif d_type == "docker_list":
                    result = str(self.docker_agent.list_containers())

                elif d_type == "google_doc_create":
                    title = instr.get("title", "Novo Doc")
                    content = instr.get("content", "")
                    result = self.google_agent.create_doc(title, content)

                elif d_type == "ide_open":
                    result = self.ide_agent.open_in_code(instr)

                elif d_type == "nlp_analyze":
                    result = self.hf_agent.ask(instr)

                else:
                    result = f"Comando '{d_type}' não reconhecido."

                execution_log.append(f"Ação: {d_type} | Resultado: {str(result)[:500]}")
                
            except Exception as e:
                execution_log.append(f"Erro no Passo {step}: {str(e)}")

        final_summary = f"Limite de {max_steps} passos atingido. Resumo:\n\n" + "\n".join(execution_log)
        self.memory.add_interaction("assistant", final_summary)
        return final_summary

    def _fallback_to_chat(self, history_context, user_input, error_msg):
        print(f"FALLBACK: {error_msg}")
        fallback_res = self.brain.ask(f"{history_context}\n\nUsuário: {user_input}")
        self.memory.add_interaction("assistant", fallback_res)
        return fallback_res

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    orch = CentralOrchestrator()
    print(orch.decide_and_execute("Qual a capital da França?"))
