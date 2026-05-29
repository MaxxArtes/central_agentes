# Project Guidelines

- **Storage Location:** All project files, virtual environments, and associated tools MUST be kept on the **D: drive** (`D:\central_agentes`).
- **Dependencies:** Python dependencies are managed in `venv/` on the D: drive and documented in `requirements.txt`.
- **Git:** The repository is initialized and should be pushed to GitHub once the remote is configured.

## Autenticação (Login)

Este projeto suporta dois métodos de autenticação para os agentes de IA:

1.  **CLI (Recomendado):** Use suas credenciais do Google logadas no terminal para limites mais altos e maior segurança.
    *   Comando: `gcloud auth application-default login`
2.  **API Key (Fallback):** Adicione sua chave no arquivo `.env` como `GOOGLE_API_KEY`.

