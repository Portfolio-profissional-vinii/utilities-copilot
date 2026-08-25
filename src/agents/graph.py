"""
Etapa 4 — Grafo de orquestração multi-agente (LangGraph).

Responsabilidade deste arquivo:
- Definir o estado compartilhado entre os nós (ex: histórico de conversa)
- Definir o nó roteador: decide se a pergunta vai para o Agente Regulatório,
  o Agente de Operações, ou ambos
- Conectar os nós em um grafo executável
- Expor uma função simples, ex: responder(pergunta: str) -> str

Ver src/agents/README.md para as perguntas-guia antes de implementar.

TODO:
- [ ] Definir o schema do estado do grafo
- [ ] Nó roteador (lógica ou LLM decidindo o caminho)
- [ ] Nó do Agente Regulatório
- [ ] Nó do Agente de Operações
- [ ] Nó de combinação de respostas (quando os dois agentes são acionados)
- [ ] Compilar e expor o grafo
"""
