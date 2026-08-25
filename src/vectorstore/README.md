# src/vectorstore/ — Etapa 2

## Objetivo
Indexar os chunks gerados na Etapa 1 em um banco vetorial local e permitir
busca híbrida (vetorial + palavra-chave).

## O que implementar aqui (sugestão de arquivos)
- `embed.py` — gera o embedding de cada chunk e insere no vector store.
- `hybrid_search.py` — combina busca vetorial (similaridade semântica) com
  BM25 (correspondência exata de palavras) e retorna um score combinado.

## Perguntas para guiar sua implementação
1. Qual modelo de embedding você vai usar? Local (`sentence-transformers`,
   ex: BGE-M3) ou via API (ex: OpenAI)? Quais os trade-offs de custo,
   privacidade e qualidade?
2. Qual vector store (Qdrant, ChromaDB, FAISS)? O que cada um oferece em
   termos de filtros por metadado (ex: filtrar só `source = modulo_7.pdf`)?
3. Por que a busca vetorial sozinha falha em perguntas do tipo "o que diz o
   Artigo 178"? Como o BM25 resolve isso?
4. Como combinar os dois rankings em um único score? (pesquise sobre
   *Reciprocal Rank Fusion*)
5. Quantos resultados (top-K) faz sentido recuperar antes de passar para o
   reranker da Etapa 3?

## Saída esperada
- Uma coleção persistida no vector store local (pasta de dados do
  Qdrant/Chroma, fora do controle de versão)
- Uma função `search(query: str, k: int) -> list[Chunk]` reutilizável pelo
  agente da Etapa 4
