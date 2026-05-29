import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Central de Agentes Carvalima", layout="wide")

def main():
    st.sidebar.title("🤖 Central de Agentes")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Menu Principal",
        ["Dashboard", "Agente LLM (Gemini)", "Automação & Scraping", "Configurações"]
    )
    
    add_vertical_space(5)
    st.sidebar.info("Carvalima Agent Central v1.0")

    if menu == "Dashboard":
        st.title("📊 Painel de Controle")
        st.write("Bem-vindo à Central de Agentes Carvalima.")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Agentes Ativos", "2")
        col2.metric("Tarefas Concluídas", "124")
        col3.metric("Tempo de Atividade", "99.9%")
        
    elif menu == "Agente LLM (Gemini)":
        st.title("🧠 Agente de Inteligência")
        st.write("Interaja com o modelo Gemini.")
        
        from agents.gemini_agent import GeminiAgent
        
        if not os.getenv("GOOGLE_API_KEY"):
            st.warning("Por favor, configure sua GOOGLE_API_KEY no arquivo .env")
        else:
            prompt = st.text_area("O que deseja perguntar ao agente?", height=100)
            if st.button("Enviar"):
                with st.spinner("Pensando..."):
                    try:
                        agent = GeminiAgent()
                        response = agent.ask(prompt)
                        st.markdown("### Resposta do Agente:")
                        st.write(response)
                    except Exception as e:
                        st.error(f"Erro ao inicializar o agente: {e}")

    elif menu == "Automação & Scraping":
        st.title("🌐 Automação Web")
        st.write("Extraia texto de qualquer página web.")
        
        from tools.scraper import SimpleScraper
        
        url = st.text_input("Insira a URL para extração de dados:", placeholder="https://exemplo.com")
        if st.button("Extrair"):
            if url:
                with st.spinner(f"Extraindo dados de {url}..."):
                    text = SimpleScraper.extract_text(url)
                    st.markdown("### Conteúdo Extraído:")
                    st.text_area("Resultado:", value=text, height=300)
            else:
                st.warning("Por favor, insira uma URL válida.")

    elif menu == "Configurações":
        st.title("⚙️ Configurações")
        st.write("Gerencie suas chaves de API e preferências.")
        google_key = st.text_input("Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
        if st.button("Salvar"):
            st.success("Configurações salvas localmente (demonstração).")

if __name__ == "__main__":
    main()
