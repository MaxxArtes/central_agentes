from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import os

class AutonomousBrowser:
    def __init__(self, model_name="gemini-1.5-flash"):
        # Usa Gemini Flash para navegação por ser mais rápido e barato
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
