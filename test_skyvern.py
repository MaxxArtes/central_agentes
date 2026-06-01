import os
from dotenv import load_dotenv
from agents.orchestrator import CentralOrchestrator
import logging

# Configura log para ver o que está acontecendo
logging.basicConfig(level=logging.INFO)

def test_skyvern_flow(command):
    load_dotenv()
    print(f"\n[TESTE SKYVERN] Comando: '{command}'")
    orch = CentralOrchestrator()
    
    # Executar fluxo completo
    print("\n--- INICIANDO LOOP AUTÔNOMO COM SKYVERN ---")
    # Limitamos a 2 passos para economizar créditos, apenas para ver a chamada ocorrer
    result = orch.decide_and_execute(command, max_steps=3)
    
    print(f"\nRESULTADO FINAL:\n{result}")

if __name__ == "__main__":
    # Teste: Um comando que sugira navegação visual complexa
    test_skyvern_flow("Use o Skyvern para entrar no site da CNN Brasil e me diga qual é a notícia principal do momento.")
