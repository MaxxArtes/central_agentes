from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

class HuggingFaceAgent:
    def __init__(self, model_id="mistralai/Mistral-7B-Instruct-v0.3"):
        """
        Agente especializado em utilizar modelos do Hugging Face via Inference API.
        Default: Mistral-7B (Versátil e rápido).
        """
        load_dotenv()
        self.token = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN")
        self.model_id = model_id
        
        if not self.token:
            print("[HuggingFace] Aviso: HUGGINGFACE_TOKEN não encontrado no .env. Algumas APIs podem falhar.")
            self.client = InferenceClient(model=self.model_id)
        else:
            self.client = InferenceClient(model=self.model_id, token=self.token)

    def ask(self, prompt, system_instructions="Você é um assistente útil e conciso."):
        try:
            # Formatação para modelos Instruct
            formatted_prompt = f"<s>[INST] {system_instructions} {prompt} [/INST]"
            
            response = self.client.text_generation(
                formatted_prompt,
                max_new_tokens=500,
                temperature=0.7,
                do_sample=True
            )
            return response.strip()
        except Exception as e:
            return f"Erro no Hugging Face Agent: {str(e)}"

    def translate(self, text, target_lang="Portuguese"):
        """Task específica de tradução usando o modelo principal ou um especializado."""
        prompt = f"Traduza o seguinte texto para {target_lang}. Retorne APENAS a tradução:\n\n{text}"
        return self.ask(prompt, system_instructions="Você é um tradutor especialista.")

if __name__ == "__main__":
    agent = HuggingFaceAgent()
    print("Testando HF Agent (Mistral):")
    print(agent.ask("Explique brevemente o que é Hugging Face."))
