import os
from groq import Groq

class GroqAgent:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("grop-api-key") or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Chave do Groq (grop-api-key) não encontrada no .env")
        
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name

    def ask(self, prompt):
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Erro no Agente Groq: {str(e)}"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    agent = GroqAgent()
    print(agent.ask("Explique brevemente o que é computação quântica."))
