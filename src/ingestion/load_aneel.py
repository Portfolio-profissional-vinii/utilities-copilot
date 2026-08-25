"""
Etapa 1 — Carga e limpeza dos indicadores estruturados da ANEEL.

Responsabilidade deste arquivo:
- Ler o(s) CSV(s) em data/raw/aneel/
- Limpar/normalizar nomes de coluna e tipos de dado
- Salvar como .parquet em data/processed/, pronto para ser consultado por
  código (pandas/SQL) no Agente de Operações da Etapa 4

Ver src/ingestion/README.md para as perguntas-guia antes de implementar.

TODO:
- [ ] Ler o(s) CSV(s) (atenção a encoding e separador)
- [ ] Normalizar nomes de colunas
- [ ] Tratar valores nulos/inconsistentes
- [ ] Salvar como .parquet
"""
