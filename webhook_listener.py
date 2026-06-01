from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Defina uma senha forte no seu .env como GITHUB_WEBHOOK_SECRET
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

@app.post("/webhook")
async def github_webhook(request: Request):
    # 1. Verificar se a requisição veio mesmo do GitHub (Segurança)
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        raise HTTPException(status_code=400, detail="Assinatura ausente.")

    body = await request.body()
    
    if GITHUB_WEBHOOK_SECRET:
        hash_object = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=body, digestmod=hashlib.sha256)
        expected_signature = "sha256=" + hash_object.hexdigest()
        if not hmac.compare_digest(signature, expected_signature):
            raise HTTPException(status_code=403, detail="Assinatura inválida.")

    # 2. Executar o Deploy
    print("\n[WEBHOOK] Push detectado no GitHub! Iniciando deploy automático...")
    
    try:
        # Comando para atualizar e reiniciar
        # Usamos o caminho absoluto /root/central_agentes
        script = """
        cd /root/central_agentes && \
        git pull origin main && \
        docker compose up -d --build && \
        docker image prune -f
        """
        subprocess.Popen(script, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        return {"status": "success", "message": "Deploy iniciado em segundo plano."}
    except Exception as e:
        print(f"[WEBHOOK] Erro ao disparar script: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Roda em uma porta diferente (ex: 9000) para não conflitar com a API principal
    uvicorn.run(app, host="0.0.0.0", port=9000)
