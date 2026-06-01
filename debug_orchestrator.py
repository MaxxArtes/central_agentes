import os
from dotenv import load_dotenv
from agents.orchestrator import CentralOrchestrator
import logging

# Configura log para ver o que está acontecendo
logging.basicConfig(level=logging.INFO)

def debug_run(command):
    load_dotenv()
    print(f"\n[DEBUG] Iniciando teste AUTÔNOMO com comando: '{command}'")
    orch = CentralOrchestrator()
    
    # Executar fluxo completo
    print("\n--- INICIANDO LOOP DE AUTONOMIA ---")
    result = orch.decide_and_execute(command, max_steps=5)
    print(f"\nRESULTADO FINAL DA TAREFA:\n{result}")

if __name__ == "__main__":
    # Teste: Notícia de hoje (01/06/2026 - No futuro do modelo, mas "hoje" no contexto)
    debug_run("Qual a cotação atual do Bitcoin em Reais? Salve em btc.txt")
