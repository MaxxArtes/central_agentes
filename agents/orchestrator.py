import os
from agents.gemini_agent import GeminiAgent
from agents.openrouter_agent import OpenRouterAgent
from tools.scraper import SimpleScraper
from tools.browser_manager import AutonomousBrowser
import asyncio
import json

class CentralOrchestrator:
    def __init__(self):
        # Agora o "Cérebro" usa o OpenRouter FREE com raciocínio habilitado
        # Isso economiza tokens e mantém alta qualidade de decisão
        self.brain = OpenRouterAgent(model_name="free")
        
        # O navegador continua usando o Gemini Flash (via OpenRouter se necessário)
        self.browser = AutonomousBrowser(model_name="google/gemini-2.0-flash-001")
    
    def decide_and_execute(self, user_input):
        system_prompt = """
        Você é o Orquestrador da Central de Agentes Carvalima.
        Sua tarefa é analisar o pedido do usuário e decidir qual ferramenta ou agente usar.
        Responda APENAS em formato JSON com os campos:
        - "decision": (string) "browser", "scraper", "chat" ou "multi"
        - "reason": (string) por que você escolheu isso
        - "instructions": (string) o que o agente deve fazer
        
        Use "browser" para pesquisas que exijam navegar em sites ou logar.
        Use "scraper" para extrair texto de uma URL específica que o usuário forneceu.
        Use "chat" para perguntas gerais de conhecimento.
        """
        
        analysis_prompt = f"{system_prompt}\n\nPedido do usuário: {user_input}"
        
        # O cérebro agora usa raciocínio (reasoning) para decidir melhor
        decision_json_raw = self.brain.ask(analysis_prompt, use_reasoning=True)
        
        # Limpa possível formatação de markdown do JSON
        decision_json_raw = decision_json_raw.replace("```json", "").replace("```", "").strip()
        
        try:
            decision = json.loads(decision_json_raw)
        except:
            return f"Orquestrador (Erro de Decisão): {decision_json_raw}"
        
        if decision["decision"] == "browser":
            return asyncio.run(self.browser.run_task(decision["instructions"]))
        elif decision["decision"] == "scraper":
            return f"Plano: {decision['reason']}. Usando Scraper para: {decision['instructions']}"
        else:
            # Para chat normal, usamos o próprio cérebro
            return self.brain.ask(user_input, use_reasoning=False)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    orch = CentralOrchestrator()
    print(orch.decide_and_execute("Vá ao google e pesquise sobre IA."))
