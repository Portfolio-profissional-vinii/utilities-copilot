"""
Etapa 2 — Busca híbrida (vetorial + BM25).

Responsabilidade deste arquivo:
- Dada uma query em texto, rodar busca vetorial no banco vetorial
- Rodar busca por palavra-chave (BM25) nos mesmos chunks
- Combinar os dois rankings em um score único
- Retornar os top-K chunks combinados

Ver src/vectorstore/README.md para as perguntas-guia antes de implementar.

TODO:
- [ ] Função de busca vetorial (usa o mesmo modelo de embedding do embed.py)
- [ ] Função de busca BM25 (ex: usando rank_bm25 ou índice do próprio
      vector store, se ele suportar)
- [ ] Função de combinação dos rankings (ex: Reciprocal Rank Fusion)
- [ ] Função search(query, k) que expõe tudo isso de forma simples
"""
