from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv

class SearchAgent:
    def __init__(self):
        """
        Agente especializado em buscas rápidas na web.
        Usa DuckDuckGo por padrão (grátis/sem chave) e tem suporte para Brave Search.
        """
        load_dotenv()
        self.brave_api_key = os.getenv("BRAVE_SEARCH_API_KEY")

    def quick_search(self, query, max_results=5):
        """Busca rápida usando DuckDuckGo."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                if not results:
                    return "Nenhum resultado encontrado."
                
                formatted_results = []
                for res in results:
                    formatted_results.append(f"🔹 {res['title']}\n🔗 {res['href']}\n📝 {res['body']}\n")
                
                return "\n".join(formatted_results)
        except Exception as e:
            return f"Erro na busca rápida (DDG): {str(e)}"

    def brave_search(self, query):
        """Busca via Brave Search API (requer chave no .env)."""
        if not self.brave_api_key:
            return "Erro: BRAVE_SEARCH_API_KEY não configurada. Use quick_search (DuckDuckGo) por enquanto."
        
        import requests
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.brave_api_key
        }
        params = {"q": query}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            # Simplificando extração do Brave
            results = data.get("web", {}).get("results", [])
            return "\n".join([f"🔸 {r['title']}\n🔗 {r['url']}" for r in results[:5]])
        except Exception as e:
            return f"Erro na busca Brave: {str(e)}"

if __name__ == "__main__":
    agent = SearchAgent()
    print("Testando Busca Rápida (DuckDuckGo):")
    print(agent.quick_search("Últimas notícias sobre IA"))
