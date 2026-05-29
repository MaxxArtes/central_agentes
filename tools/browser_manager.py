from browser_use import Agent
import asyncio
import os

class AutonomousBrowser:
    def __init__(self, model_name="openrouter/free"):
        # Usamos o wrapper LangChain para OpenAI apontando para o OpenRouter
        # Este modelo é gratuito e muito estável para navegação
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv("api-key-openrouter") or os.getenv("OPENROUTER_API_KEY")
        
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model="openrouter/free", # Forçamos o modelo gratuito documentado
            default_headers={
                "HTTP-Referer": "https://github.com/MaxxArtes/central_agentes",
                "X-Title": "Central de Agentes Carvalima"
            }
        )
        # Patch para compatibilidade com browser-use
        # Usamos object.__setattr__ para burlar a validação do Pydantic no LangChain
        if not hasattr(self.llm, 'provider'):
            object.__setattr__(self.llm, 'provider', 'openai')
        if not hasattr(self.llm, 'model_name'):
            object.__setattr__(self.llm, 'model_name', 'openrouter/free')
    
    async def run_task(self, task_description):
        try:
            agent = Agent(
                task=task_description,
                llm=self.llm,
            )
            history = await agent.run()
            # O result do browser-use agora é extraído do histórico final
            result = history.final_result()
            return result if result else "A navegação foi concluída, mas nenhum resultado específico foi retornado."
        except Exception as e:
            return f"Erro na navegação autônoma: {str(e)}"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    browser = AutonomousBrowser()
    asyncio.run(browser.run_task("Vá ao google.com"))
