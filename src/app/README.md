# src/app/ — Etapa 5

## Objetivo
Interface Streamlit com duas abas: chat do copiloto (Etapa 4) e um
dashboard de indicadores da ANEEL.

## O que implementar aqui (sugestão de arquivos)
- `app.py` — ponto de entrada do Streamlit (`streamlit run src/app/app.py`)
- `chat_tab.py` — aba de chat, chama o grafo definido em `src/agents/`
- `dashboard_tab.py` — aba com gráficos/tabelas dos indicadores da ANEEL

## Perguntas para guiar sua implementação
1. Como manter o histórico de mensagens do chat entre interações no
   Streamlit? (dica: `st.session_state`)
2. Como exibir a citação da fonte (documento + página) de forma clara na
   interface, sem poluir a resposta?
3. Que visualizações fazem sentido no dashboard para um consultor de
   Utilities (ex: DEC/FEC por região, evolução no tempo)?
4. Como você trata erros (ex: PDF sem resposta relevante, agente de
   operações sem dado para a região pedida)?

## Saída esperada
- App Streamlit funcional localmente com `streamlit run src/app/app.py`
