from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import os

class AutonomousBrowser:
    def __init__(self, model_name="google/gemini-2.0-flash-001"):
        # Importações dentro do init para evitar conflitos de versão globais
        api_key = os.getenv("api-key-openrouter") or os.getenv("OPENROUTER_API_KEY")
        
        # Mapeamento de nomes para garantir compatibilidade
        if "gemini-1.5-flash" in model_name: model_name = "google/gemini-2.0-flash-001"
        
        if api_key:
            # Para o browser-use, o melhor é usar o ChatOpenAI padrão do LangChain
            # configurado para o OpenRouter
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                model=model_name,
                # Desativa verificações específicas que podem causar o erro 'provider'
                default_headers={"HTTP-Referer": "https://github.com/MaxxArtes/central_agentes"}
            )
        else:
            # Fallback para Gemini direto (via CLI ou Key)
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
    async def run_task(self, task_description):
        agent = Agent(
            task=task_description,
            llm=self.llm,
        )
        result = await agent.run()
        return result

if __name__ == "__main__":
    # Teste rápido
    from dotenv import load_dotenv
    load_dotenv()
    browser = AutonomousBrowser()
    asyncio.run(browser.run_task("Vá ao google.com e procure por 'notícias de tecnologia'"))
