import google.generativeai as genai
import os
from dotenv import load_dotenv

def test_adc_auth():
    print("--- Testando Autenticação ADC (CLI) ---")
    # Limpa a chave do ambiente para forçar o uso da CLI
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]
    if "GOOGLE_API_KEY" in os.environ:
        del os.environ["GOOGLE_API_KEY"]
    
    try:
        genai.configure()
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Diga 'OK' se você consegue me ouvir via CLI.")
        print(f"Sucesso! Resposta: {response.text}")
    except Exception as e:
        print(f"Falha na autenticação via CLI: {e}")

if __name__ == "__main__":
    test_adc_auth()
