"""
Etapa 4 — Agente de Operações.

Responsabilidade deste arquivo:
- Definir as "tools"/funções que o LLM pode chamar sobre o dataframe da
  ANEEL (data/processed/aneel_indicadores.parquet)
- Expor essas funções via function calling para o LLM
- Executar a consulta real (pandas/SQL) e devolver o resultado numérico
  exato para o LLM formular a resposta final

Ver src/agents/README.md para as perguntas-guia antes de implementar.

TODO:
- [ ] Carregar o parquet da ANEEL
- [ ] Definir as funções de consulta (ex: consultar_indicador(regiao, ano,
      indicador))
- [ ] Registrar essas funções como tools para o LLM
- [ ] Lógica de execução da tool escolhida pelo LLM
"""
