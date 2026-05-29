from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import os

class AutonomousBrowser:
    def __init__(self, model_name="google/gemini-2.0-flash-001"):
        # Se a chave do OpenRouter estiver presente, usamos ela via OpenAI wrapper no LangChain
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv("api-key-openrouter") or os.getenv("OPENROUTER_API_KEY")
        
        if api_key:
            self.llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                model=model_name
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
