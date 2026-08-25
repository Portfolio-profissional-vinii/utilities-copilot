# src/reranking/ — Etapa 3

## Objetivo
Pegar os top-K resultados da busca híbrida (Etapa 2) e reordená-los por
relevância real à pergunta, usando um cross-encoder.

## O que implementar aqui (sugestão de arquivos)
- `rerank.py` — recebe (query, lista de chunks) e devolve a lista reordenada
  e cortada para os N mais relevantes.

## Perguntas para guiar sua implementação
1. Qual a diferença entre um *bi-encoder* (usado nos embeddings da Etapa 2)
   e um *cross-encoder* (usado no reranker)? Por que o cross-encoder é mais
   preciso, porém mais caro?
2. Por que rodar o reranker só nos top-10/20 candidatos, e não no dataset
   inteiro?
3. Qual modelo de reranker você vai usar? (ex: `BAAI/bge-reranker-base`,
   rodando localmente na sua GPU via `transformers`/`sentence-transformers`)
4. Depois do reranking, quantos chunks você vai efetivamente enviar ao LLM
   final? Como esse número afeta custo e qualidade da resposta?

## Saída esperada
- Uma função `rerank(query: str, candidates: list[Chunk], top_n: int) ->
  list[Chunk]` usada pelo Agente Regulatório na Etapa 4
