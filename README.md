# Utilities Regulatory Copilot

Copiloto para consultoria em Utilities (energia/saneamento/gás): une busca
em normas regulatórias (PRODIST) com dados estruturados da ANEEL, usando
RAG avançado + arquitetura multi-agente.

Esta é a **estrutura vazia** do projeto — cada pasta tem seu próprio
`README.md` explicando o que deve ser implementado ali e por quê, mas o
código é seu, feito manualmente com apoio de IA.

## Ordem sugerida de implementação (Etapas)

1. `src/ingestion/`   → extração de PDFs + semantic chunking + carga do CSV
2. `src/vectorstore/` → embeddings + banco vetorial + busca híbrida (BM25)
3. `src/reranking/`   → reordenação dos resultados com cross-encoder
4. `src/agents/`      → orquestração multi-agente (LangGraph) + function calling
5. `src/app/`         → interface Streamlit
6. `docker/`          → containerização de tudo

## Antes de começar

- Baixe os PDFs do PRODIST (Módulos 3 e 7) → `data/raw/prodist/`
- Baixe o(s) CSV(s) de indicadores da ANEEL (DEC/FEC) → `data/raw/aneel/`
- Copie `.env.example` para `.env` e preencha suas chaves/config

## Como usar este repositório para aprender

Para cada etapa: abra o `README.md` da pasta correspondente, leia os
conceitos e as perguntas-guia, e tente implementar sozinho. Use a IA para
tirar dúvidas pontuais ou revisar o que você escreveu — não para gerar o
arquivo inteiro de uma vez.
