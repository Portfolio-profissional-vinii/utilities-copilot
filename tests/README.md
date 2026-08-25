# tests/

Testes unitários para cada etapa. Sugestão de organização, espelhando
`src/`:

- `test_ingestion.py`
- `test_vectorstore.py`
- `test_reranking.py`
- `test_agents.py`

Dica: teste o chunking com um texto curto controlado por você (não o PDF
inteiro) para validar que as fronteiras de "Artigo" e o overlap estão
funcionando como esperado.
