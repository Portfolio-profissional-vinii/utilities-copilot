import os
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


st.set_page_config(
    page_title="Utilities Copilot",
    page_icon="⚡",
    layout="wide",
)

from src.app.dashboard_tab import render_dashboard_tab
from src.agents.graph import CopilotOrchestrator

st.sidebar.title("🔑 Autenticação")

if "google_api_key" not in st.session_state:
    st.session_state.google_api_key = ""


user_api_key = st.sidebar.text_input(
    "Sua Gemini API Key",
    type="password",
    value=st.session_state.google_api_key,
    help="Obtenha sua chave em https://aistudio.google.com/",
)

if user_api_key:
    st.session_state.google_api_key = user_api_key
    os.environ["GOOGLE_API_KEY"] = user_api_key

st.title("⚡ Utilities Copilot")

tab_chat, tab_dash = st.tabs(
    [
        "💬 Chat Regulatório & Operacional",
        "📊 Dashboard de Indicadores",
    ]
)

with tab_chat:

    st.header("Assistente Virtual")

    # Inicializa histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if not st.session_state.google_api_key:

        st.info(
            "Insira sua **Gemini API Key** na barra lateral "
            "para utilizar o Copiloto."
        )

    else:
        os.environ["GOOGLE_API_KEY"] = (
            st.session_state.google_api_key
        )

        @st.cache_resource
        def carregar_orquestrador(api_key: str):
            os.environ["GOOGLE_API_KEY"] = api_key
            return CopilotOrchestrator()

        try:

            orchestrator = carregar_orquestrador(
                st.session_state.google_api_key
            )

        except Exception as e:

            st.error(
                f"Não foi possível inicializar o Copiloto: {e}"
            )

            orchestrator = None

        if orchestrator is not None:

            prompt = st.chat_input(
                "Pergunte sobre regulamentação ou dados operacionais..."
            )

            if prompt:

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": prompt,
                    }
                )

                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):

                    with st.spinner(
                        "Analisando solicitação..."
                    ):

                        try:

                            resposta = orchestrator.responder(
                                prompt
                            )

                            st.markdown(resposta)


                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": resposta,
                                }
                            )


                        except Exception as e:

                            st.error(
                                f"Erro ao processar a solicitação: {e}"
                            )

with tab_dash:

    render_dashboard_tab()