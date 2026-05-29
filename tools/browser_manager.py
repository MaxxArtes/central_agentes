from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import os

class AutonomousBrowser:
    def __init__(self, model_name="google/gemini-2.0-flash-001"):
        # Usamos uma forma mais compatível de carregar o modelo para evitar conflitos de versão
        api_key = os.getenv("api-key-openrouter") or os.getenv("OPENROUTER_API_KEY")
        
        if api_key:
            try:
                # Tenta usar o wrapper oficial se disponível
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key,
                    model=model_name
                )
            except (ImportError, Exception):
                # Fallback: Usamos o wrapper da comunidade ou direto se o anterior falhar
                from langchain_community.chat_models import ChatOpenAI as CommunityChatOpenAI
                self.llm = CommunityChatOpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    openai_api_key=api_key,
                    model_name=model_name
                )
        else:
            # Fallback para Gemini direto
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(model=model_name)
    
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
