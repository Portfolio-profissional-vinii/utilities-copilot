"""
Etapa 2 — Geração de embeddings e indexação no vector store.

Responsabilidade deste arquivo:
- Ler data/processed/chunks.jsonl
- Gerar o embedding de cada chunk
- Inserir no banco vetorial local (Qdrant/Chroma), junto com os metadados
  (source, page, id) para recuperação posterior

Ver src/vectorstore/README.md para as perguntas-guia antes de implementar.

TODO:
- [ ] Escolher e configurar o modelo de embedding
- [ ] Escolher e configurar o vector store local
- [ ] Função para indexar a lista de chunks
- [ ] Decidir como lidar com re-indexação (evitar duplicar ao rodar de novo)
"""
