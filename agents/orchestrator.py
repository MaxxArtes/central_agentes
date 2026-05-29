import os
from agents.gemini_agent import GeminiAgent
from agents.openrouter_agent import OpenRouterAgent
from tools.scraper import SimpleScraper
from tools.browser_manager import AutonomousBrowser
import asyncio
import json

class CentralOrchestrator:
    def __init__(self):
        # Usamos o GeminiAgent como "Cérebro"
        # Ele é híbrido: Tenta usar seu Login Pro (CLI) primeiro, 
        # e se der erro de chave, pula automaticamente para o OpenRouter.
        self.brain = GeminiAgent(model_name="gemini-1.5-pro")
        
        # O navegador também usa a lógica híbrida para não travar
        self.browser = AutonomousBrowser(model_name="google/gemini-2.0-flash-001")
    
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
        
        # Se o cérebro retornar um erro em vez de JSON
        if "Erro" in decision_json_raw and "{" not in decision_json_raw:
             return decision_json_raw

        # Limpa possível formatação de markdown do JSON
        decision_json_raw = decision_json_raw.replace("```json", "").replace("```", "").strip()
        
        try:
            decision = json.loads(decision_json_raw)
        except:
            return f"Orquestrador: Não consegui processar o plano.\nResposta: {decision_json_raw}"
        
        if decision["decision"] == "browser":
            return asyncio.run(self.browser.run_task(decision["instructions"]))
        elif decision["decision"] == "scraper":
            return f"Plano: {decision['reason']}. Usando Scraper para: {decision['instructions']}"
        else:
            return self.brain.ask(user_input)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    orch = CentralOrchestrator()
    print(orch.decide_and_execute("Qual a temperatura em São Paulo?"))
