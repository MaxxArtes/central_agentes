import os
from agents.gemini_agent import GeminiAgent
from agents.openrouter_agent import OpenRouterAgent
from tools.scraper import SimpleScraper
from tools.browser_manager import AutonomousBrowser
import asyncio
import json

class CentralOrchestrator:
    def __init__(self):
        # O "Cérebro" é o Gemini Pro via CLI (limites altos)
        self.brain = GeminiAgent(model_name="gemini-1.5-pro")
        self.browser = AutonomousBrowser(model_name="gemini-1.5-flash")
    
    def decide_and_execute(self, user_input):
        system_prompt = """
        Você é o Orquestrador da Central de Agentes Carvalima.
        Sua tarefa é analisar o pedido do usuário e decidir qual ferramenta ou agente usar.
        Responda APENAS em formato JSON com os campos:
        - "decision": (string) "browser", "scraper", "chat" ou "multi"
        - "reason": (string) por que você escolheu isso
        - "instructions": (string) o que o agente deve fazer
        """
        
        analysis_prompt = f"{system_prompt}\n\nPedido do usuário: {user_input}"
        decision_json_raw = self.brain.ask(analysis_prompt)
        
        # Limpa possível formatação de markdown do JSON
        decision_json_raw = decision_json_raw.replace("```json", "").replace("```", "").strip()
        
        try:
            decision = json.loads(decision_json_raw)
        except:
            return f"Erro na orquestração: O cérebro não retornou um plano válido.\nResposta: {decision_json_raw}"
        
        if decision["decision"] == "browser":
            return asyncio.run(self.browser.run_task(decision["instructions"]))
        elif decision["decision"] == "scraper":
            # Extrai URL se necessário ou usa o scraper simples
            return f"Plano: {decision['reason']}. Usando Scraper para: {decision['instructions']}"
        else:
            return self.brain.ask(user_input)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    orch = CentralOrchestrator()
    print(orch.decide_and_execute("Pesquise o preço do iPhone 15 no site da Amazon e me dê o valor."))
