from openai import OpenAI
import os
from dotenv import load_dotenv

def test_openrouter():
    load_dotenv()
    api_key = os.getenv("api-key-openrouter")
    print(f"Testando chave: {api_key[:10]}...")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": "Diga 'OK'."}]
        )
        print(f"Sucesso! Resposta: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Erro no OpenRouter: {e}")

if __name__ == "__main__":
    test_openrouter()
