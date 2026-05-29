import asyncio
from playwright.async_api import async_playwright
import os

async def check_session():
    # Caminho padrão do Chrome no Windows
    user_data_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    
    async with async_playwright() as p:
        print(f"Tentando abrir contexto persistente em: {user_data_dir}")
        try:
            # Tenta usar o perfil 'Default'
            context = await p.chromium.launch_persistent_context(
                user_data_dir,
                executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                headless=False, # Abre visível para o usuário ver se precisar
                args=['--profile-directory=Default']
            )
            page = await context.new_page()
            await page.goto("https://aistudio.google.com/app/apikey")
            await asyncio.sleep(5) # Espera carregar
            
            title = await page.title()
            url = await page.url()
            print(f"Página carregada: {title}")
            print(f"URL atual: {url}")
            
            if "login" in url.lower() or "signin" in url.lower():
                print("Não logado. Sessão não encontrada no perfil Default.")
            else:
                print("Sessão ativa detectada!")
                # Tenta pegar a chave da tela se estiver logado
                # (Lógica para extrair a chave se necessário)
            
            await context.close()
        except Exception as e:
            print(f"Erro ao acessar perfil do Chrome: {e}")

if __name__ == "__main__":
    asyncio.run(check_session())
