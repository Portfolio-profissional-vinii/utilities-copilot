import streamlit as st

def render_chat_tab(orchestrator):
    st.subheader("💬 Chat Inteligente")
    st.caption("Consulte normativas do PRODIST ou dados operacionais da ANEEL em linguagem natural.")

    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    # Exibe o histórico do chat
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pergunta = st.chat_input("Digite sua dúvida sobre regras ou dados da ANEEL...")

    if pergunta:
        with st.chat_message("user"):
            st.markdown(pergunta)
        
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        
        with st.chat_message("assistant"):
            with st.spinner("Analisando e consultando bases de dados..."):
                try:
                    resposta = orchestrator.responder(pergunta)
                    st.markdown(resposta)
                    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
                except Exception as e:
                    st.error(f"Erro ao processar resposta: {e}")