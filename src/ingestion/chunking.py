"""
Etapa 1 — Semantic Chunking dos textos extraídos.

Responsabilidade deste arquivo:
- Ler os JSONs gerados por extract_pdf.py
- Quebrar o texto em chunks: primeiro por fronteira semântica (ex: "Art. X"),
  depois por tamanho de token com overlap, se o bloco ainda for grande
- Salvar tudo em data/processed/chunks.jsonl, com metadados (source, page)

Ver src/ingestion/README.md para as perguntas-guia antes de implementar.

TODO:
- [ ] Regex ou lógica para identificar fronteiras naturais do texto
- [ ] Função de corte por tamanho de token com overlap
- [ ] Definir tamanho de chunk e overlap (e justificar a escolha)
- [ ] Gerar um id único por chunk
- [ ] Salvar em formato .jsonl
"""
