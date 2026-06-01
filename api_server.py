from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.orchestrator import CentralOrchestrator
import uvicorn
import asyncio
from dotenv import load_dotenv

# Carrega chaves
load_dotenv()

app = FastAPI(title="Central de Agentes - Gateway para Bubble")
orchestrator = CentralOrchestrator()

class AgentRequest(BaseModel):
    command: str

@app.get("/")
def home():
    return {"status": "online", "message": "Central de Agentes Carvalima pronta para receber pedidos do Bubble!"}

@app.post("/execute")
async def execute_command(request: AgentRequest):
    """
    Recebe um comando do Bubble, executa o Orquestrador e devolve a resposta.
    """
    if not request.command:
        raise HTTPException(status_code=400, detail="Comando vazio.")
    
    print(f"\n[API] Recebido do Bubble: {request.command}")
    
    try:
        # Roda o orquestrador em modo Manus (Autônomo)
        # Como o Bubble espera uma resposta, definimos um limite de passos
        result = orchestrator.decide_and_execute(request.command, max_steps=5)
        
        return {
            "response": result,
            "status": "success"
        }
    except Exception as e:
        print(f"[API] Erro: {str(e)}")
        return {
            "response": f"Ocorreu um erro ao processar sua solicitação: {str(e)}",
            "status": "error"
        }

if __name__ == "__main__":
    # Roda o servidor local na porta 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
