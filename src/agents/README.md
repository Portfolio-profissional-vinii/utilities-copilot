# src/agents/ — Etapa 4

## Objetivo
Orquestrar dois agentes especializados com LangGraph:
- **Agente Regulatório**: consulta o RAG (Etapas 1-3) e responde citando
  a fonte (documento + página).
- **Agente de Operações**: roda consultas (pandas/SQL) sobre o parquet da
  ANEEL via function calling.

## O que implementar aqui (sugestão de arquivos)
- `regulatory_agent.py` — lógica do agente que usa `search()` +
  `rerank()` e monta o prompt final com as fontes citadas.
- `operations_agent.py` — define as "tools"/funções que o LLM pode chamar
  sobre o dataframe da ANEEL (ex: `consultar_indicador(regiao, ano,
  indicador)`).
- `graph.py` — define o grafo do LangGraph: nó roteador (decide qual agente
  chamar) + os dois agentes + (se precisar) um nó final que combina as
  respostas.

## Perguntas para guiar sua implementação
1. Como o roteador decide se a pergunta é regulatória, operacional, ou as
   duas? Que sinais no texto da pergunta indicam isso?
2. O que é *function calling* e por que é mais confiável do que pedir para
   o LLM "calcular" um número sozinho?
3. Como você estrutura o estado (state) do grafo para manter histórico de
   conversa entre chamadas?
4. Como cada agente formata a citação da fonte na resposta final?
5. O que acontece se a pergunta exigir os dois agentes juntos (ex: "o
   cliente X está fora do limite regulatório de DEC")? Como combinar as
   duas respostas em uma única resposta coerente?

## Saída esperada
- Um grafo executável que recebe uma pergunta em linguagem natural e
  devolve uma resposta final, roteando internamente para o(s) agente(s)
  corretos
