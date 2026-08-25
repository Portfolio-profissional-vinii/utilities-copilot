"""
Etapa 3 — Reranking dos resultados da busca híbrida.

Responsabilidade deste arquivo:
- Receber (query, lista de chunks candidatos) vindos da hybrid_search
- Rodar um cross-encoder para avaliar a relevância real de cada par
  (query, chunk)
- Retornar a lista reordenada, cortada para os N mais relevantes

Ver src/reranking/README.md para as perguntas-guia antes de implementar.

TODO:
- [ ] Carregar o modelo de reranking escolhido
- [ ] Função rerank(query, candidates, top_n) que devolve a lista reordenada
- [ ] Definir quantos candidatos entram (top-K da busca) e quantos saem
      (top-N depois do rerank)
"""
