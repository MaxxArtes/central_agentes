import os
from dotenv import load_dotenv
from agents.orchestrator import CentralOrchestrator
import logging

# Configura log para ver o que está acontecendo
logging.basicConfig(level=logging.INFO)

def debug_run(command):
    load_dotenv()
    print(f"\n[DEBUG] Iniciando teste com comando: '{command}'")
    orch = CentralOrchestrator()
    
    # 1. Testar o cérebro (Gemini CLI)
    print("\n--- 1. TESTANDO DECISÃO DO CÉREBRO ---")
    history_context = orch.memory.get_context_summary()
    system_prompt = f"Você é o Orquestrador. Responda APENAS em JSON.\n{history_context}"
    analysis_prompt = f"{system_prompt}\n\nPedido: {command}"
    
    decision_raw = orch.brain.ask(analysis_prompt)
    print(f"RAW DECISION FROM CLI:\n'{decision_raw}'")
    
    # 2. Executar fluxo completo
    print("\n--- 2. EXECUTANDO FLUXO COMPLETO ---")
    result = orch.decide_and_execute(command)
    print(f"\nRESULTADO FINAL:\n'{result}'")

if __name__ == "__main__":
    debug_run("pesquise mcp para interagir com IA")
