import json
import os
from agents.google_agent import GoogleAgent
from googleapiclient.http import MediaInMemoryUpload

class ColabAgent:
    def __init__(self):
        """
        Agente para criar e gerenciar Notebooks do Google Colab.
        Baseia-se no GoogleAgent para acesso ao Drive.
        """
        self.google = GoogleAgent()

    def is_active(self):
        return self.google.is_active()

    def create_notebook(self, title, description=""):
        """Cria um arquivo .ipynb básico no Google Drive."""
        if not self.is_active(): return "Google Drive não autenticado."
        
        # Estrutura básica de um Jupyter Notebook
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"# {title}\n", f"{description}\n", "\n*Gerado automaticamente pela Central de Agentes Carvalima*"]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["# Escreva seu código aqui\n", "print('Olá do Google Colab!')"]
                }
            ],
            "metadata": {
                "colab": {"provenance": []},
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python"}
            },
            "nbformat": 4,
            "nbformat_minor": 0
        }

        try:
            file_metadata = {
                'name': f"{title}.ipynb",
                'mimeType': 'application/x-ipynb+json'
            }
            media = MediaInMemoryUpload(
                json.dumps(notebook_content).encode('utf-8'),
                mimetype='application/x-ipynb+json',
                resumable=True
            )
            
            file = self.google.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file.get('id')
            colab_url = f"https://colab.research.google.com/drive/{file_id}"
            
            return f"Notebook '{title}' criado com sucesso!\n🔗 Abra aqui: {colab_url}"
        except Exception as e:
            return f"Erro ao criar notebook no Colab: {str(e)}"

if __name__ == "__main__":
    agent = ColabAgent()
    if agent.is_active():
        print("Colab Agent pronto!")
        # print(agent.create_notebook("Análise de Teste", "Notebook gerado para validar integração."))
    else:
        print("Aguardando autenticação Google Drive...")
