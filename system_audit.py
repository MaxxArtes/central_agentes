import os
import asyncio
from dotenv import load_dotenv
from agents.orchestrator import CentralOrchestrator

def audit_log(msg):
    print(f"[AUDITORIA] {msg}")

async def run_audit():
    load_dotenv()
    orch = CentralOrchestrator()
    
    # 1. Auditoria de Conectividade e Credenciais
    audit_log("--- FASE 1: Verificação de Conectividade ---")
    
    agents_to_check = {
        "Base44": orch.base44_agent.is_active(),
        "Apify": orch.apify_agent.is_active(),
        "Skyvern": orch.skyvern_agent.is_active(),
        "GitHub": orch.github_agent.is_active(),
        "Docker": orch.docker_agent.is_active(),
        "Database (Supabase)": orch.db_agent.is_active(),
        "Google Workspace": orch.google_agent.is_active()
    }
    
    for name, active in agents_to_check.items():
        status = "✅ ATIVO" if active else "❌ INATIVO/NÃO CONFIGURADO"
        audit_log(f"{name}: {status}")

    # 2. Testes Funcionais Isolados
    audit_log("\n--- FASE 2: Testes Funcionais Isolados ---")
    
    # Filesystem
    try:
        res = orch.file_agent.write_file("audit_test.txt", "Teste de auditoria")
        audit_log(f"FileAgent (Write): {res}")
        content = orch.file_agent.read_file("audit_test.txt")
        audit_log(f"FileAgent (Read): {'✅ OK' if content == 'Teste de auditoria' else '❌ Erro'}")
        orch.file_agent.delete_file("audit_test.txt")
    except Exception as e:
        audit_log(f"FileAgent: ❌ Erro: {e}")

    # Apify (Check Credits)
    try:
        credits = orch.apify_agent.get_remaining_credits()
        audit_log(f"Apify (Créditos): ${credits}")
    except Exception as e:
        audit_log(f"Apify: ❌ Erro ao consultar créditos: {e}")

    # 3. Teste de Stress do Orquestrador (Loop Autônomo)
    audit_log("\n--- FASE 3: Teste de Stress do Orquestrador (Modo Manus) ---")
    complex_command = "Crie um arquivo chamado 'saudacao.txt' com a frase 'Olá Mundo', depois liste os arquivos do diretório e me diga se o arquivo foi criado com sucesso."
    
    audit_log(f"Executando comando complexo: '{complex_command}'")
    result = orch.decide_and_execute(complex_command, max_steps=5)
    audit_log(f"Resultado Final do Orquestrador:\n{result}")

if __name__ == "__main__":
    asyncio.run(run_audit())
