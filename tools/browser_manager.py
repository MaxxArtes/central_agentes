from browser_use import Agent
import asyncio
import os

class AutonomousBrowser:
    def __init__(self, model_name="openrouter/free"):
        # Usamos o modelo free via LangChain para o navegador
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv("api-key-openrouter") or os.getenv("OPENROUTER_API_KEY")
        
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model=model_name,
            default_headers={
                "HTTP-Referer": "https://github.com/MaxxArtes/central_agentes",
                "X-Title": "Central de Agentes Carvalima"
            }
        )
    
    async def run_task(self, task_description):
        agent = Agent(
            task=task_description,
            llm=self.llm,
        )
        result = await agent.run()
        return result

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    browser = AutonomousBrowser()
    asyncio.run(browser.run_task("Vá ao google.com e procure por 'notícias'"))
