"""
Etapa 4 — Agente Regulatório.

Responsabilidade deste arquivo:
- Receber uma pergunta do usuário
- Usar hybrid_search() + rerank() para recuperar os trechos mais relevantes
  do PRODIST
- Montar o prompt final para o LLM, incluindo os trechos recuperados
- Formatar a resposta citando a fonte (documento + página)

Ver src/agents/README.md para as perguntas-guia antes de implementar.

TODO:
- [ ] Função que monta o prompt com os chunks recuperados
- [ ] Chamada ao LLM
- [ ] Extração/formatação das citações de fonte na resposta
"""
