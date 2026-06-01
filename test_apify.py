import os
from dotenv import load_dotenv
from agents.orchestrator import CentralOrchestrator
import logging

# Configura log para ver o que está acontecendo
logging.basicConfig(level=logging.INFO)

def test_apify_flow(command):
    load_dotenv()
    print(f"\n[TESTE APIFY] Comando: '{command}'")
    orch = CentralOrchestrator()
    
    # Verifica crédito inicial
    initial_credits = orch.apify_agent.get_remaining_credits()
    print(f"Créditos Iniciais: ${initial_credits}")
    
    if initial_credits <= 0:
        print("Erro: Token pode estar inválido ou sem créditos.")
        return

    # Executar fluxo completo
    print("\n--- INICIANDO LOOP AUTÔNOMO COM APIFY ---")
    result = orch.decide_and_execute(command, max_steps=3)
    
    # Verifica crédito final
    final_credits = orch.apify_agent.get_remaining_credits()
    print(f"\nCréditos Finais: ${final_credits}")
    print(f"Custo da Operação: ${round(initial_credits - final_credits, 4)}")
    
    print(f"\nRESULTADO FINAL:\n{result}")

if __name__ == "__main__":
    # Teste: Um comando que o Orquestrador deve preferir Apify
    # Google Maps é um ótimo exemplo, pois é difícil de raspar via browser comum
    test_apify_flow("Busque 3 pizzarias em São Paulo usando o Apify e me diga os nomes.")
