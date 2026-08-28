import os
import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

st.set_page_config(page_title="Utilities Copilot", page_icon="⚡", layout="wide")

# Barra Lateral - Entrada da API Key
st.sidebar.title("🔑 Autenticação")
user_api_key = st.sidebar.text_input(
    "Sua Gemini API Key", 
    type="password", 
    help="Obtenha sua chave gratuita em https://aistudio.google.com/"
)

if user_api_key:
    os.environ["GOOGLE_API_KEY"] = user_api_key

# Trava a aplicação se a chave não for informada
if not os.environ.get("GOOGLE_API_KEY"):
    st.info("👈 Insira sua **Gemini API Key** na barra lateral para começar.")
    st.stop()

# Importação dos agentes após a definição da chave
from src.agents.graph import CopilotOrchestrator

@st.cache_resource
def carregar_orquestrador(api_key: str):
    return CopilotOrchestrator()

orchestrator = carregar_orquestrador(os.environ["GOOGLE_API_KEY"])

st.title("⚡ Utilities Copilot - Total Utiliti")

tab_chat, tab_dash = st.tabs(["💬 Chat Regulatório & Operacional", "📊 Dashboard de Indicadores"])

with tab_chat:
    st.header("Assistente Virtual")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Pergunte sobre regulamentação ou dados operacionais..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analisando solicitação..."):
                resposta = orchestrator.processar_pergunta(prompt)
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})

with tab_dash:
    st.header("Indicadores Operacionais (DECP e FECP)")
    st.info("Visão geral dos dados de interrupção de energia.")