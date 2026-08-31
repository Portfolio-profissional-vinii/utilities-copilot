# Utilities Regulatory Copilot

Copiloto de IA especializado no setor elétrico, desenvolvido para auxiliar na consulta e análise de normativas regulatórias da ANEEL, como o PRODIST e a REN ANEEL nº 1.000/2021, combinando **RAG híbrido + re-ranking + arquitetura multi-agente.**

O sistema permite consultar as normas em linguagem natural, encontrando informações relevantes em documentos regulatórios extensos, além de realizar consultas sobre **dados operacionais estruturados**. Um agente roteador identifica automaticamente o tipo de solicitação e direciona a pergunta para o agente especializado.

Por exemplo:

• "O que é o indicador DIC?"

• "Quando a distribuidora deve compensar o consumidor por violação do DIC?"

• "Quais são os limites para compensação por violação dos indicadores de continuidade?"

• "Qual foi o valor médio do indicador DEC em 2020?"

A arquitetura combina **busca semântica (Dense Retrieval), busca lexical com BM25, Hybrid Search com RRF, re-ranking, Qdrant, LangGraph e Google Gemini**, permitindo respostas fundamentadas no contexto recuperado e com referência à normativa, módulo e página.

---

## Visão Geral

| Tipo de pergunta | Exemplo | Agente responsável |
|---|---|---|
| **Regulatória** | "Quais os requisitos de proteção para subestações de MT/AT?" | `regulatory_agent` (RAG + Qdrant + BM25 + Reranker) |
| **Operacional** | "Qual a média do FEC da distribuidora CEA em 2021?" | `operations_agent` (Text-to-SQL via DuckDB) |

Um **agente roteador** (LLM com temperatura 0) classifica a intenção da pergunta e direciona o fluxo para o especialista correto, dentro de um grafo de orquestração (`CopilotOrchestrator`).

---

## Arquitetura

<img width="2720" height="1696" alt="arquitetura_utilities_copilot" src="https://github.com/user-attachments/assets/c055e4b0-d0a3-4fca-9587-3ac2833b9db7" />

### Busca Híbrida (RAG)

A busca regulatória combina duas estratégias de recuperação, fundidas manualmente via **Reciprocal Rank Fusion (RRF)**:

1. **Busca densa (semântica)** — embeddings via `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (384 dimensões), indexados no **Qdrant**.
2. **Busca lexical (BM25)** — via `rank_bm25`, com tokenização customizada para português.
3. **Fusão RRF** — combina os rankings das duas fontes (`RRF_K = 60`, conforme Cormack et al., 2009).
4. **Reranking** — os candidatos combinados passam por um **Cross-Encoder** (`BAAI/bge-reranker-base`) para reordenação final por relevância semântica real.

### Text-to-SQL (Dados Operacionais)

O `operations_agent` converte a pergunta do usuário em uma consulta SQL válida para **DuckDB**, executada diretamente sobre um arquivo **Parquet** com os indicadores de continuidade da ANEEL (DEC, FEC, DECXNC, FECIPC, etc.), e depois formula a resposta final em linguagem natural com base nos dados retornados.

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Orquestração de agentes | LangChain / LangGraph |
| LLM | Google Gemini (`gemini-3.6-flash`) via `langchain-google-genai` |
| Embeddings | HuggingFace `paraphrase-multilingual-MiniLM-L12-v2` |
| Banco vetorial | Qdrant |
| Busca lexical | `rank_bm25` |
| Reranking | `sentence-transformers` (Cross-Encoder `bge-reranker-base`) |
| Dados estruturados | DuckDB + Parquet + Pandas |
| Extração de PDF | PyMuPDF (`pymupdf`) |
| Interface | Streamlit |
| Containerização | Docker / Docker Compose |
| Testes | Pytest |

---

## 📂 Estrutura do Projeto

```
utilities-copilot/
│
├── .vscode/
│   └── settings.json
│
├── data/
│   ├── processed/              # Dados processados (parquet, csv, json)
│   │   ├── aneel_indicadores.parquet
│   │   ├── aneel_indicadores_clean.csv
│   │   ├── *_chunks.json       # chunks dos módulos PRODIST
│   │   └── *_extraido.json     # texto extraído dos PDFs
│   │
│   ├── raw/
│   │   ├── aneel/
│   │   │   └── indicadores-continuidade-coletivos-2020-2029.csv
│   │   └── prodist/             # PDFs dos módulos PRODIST (1–11)
│   │       └── *.pdf
│   │
│   └── vectorstore/
│       └── bm25.pkl
│
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
│
├── notebooks/
│   ├── 01_explorar_pdf.ipynb
│   ├── 02_test_chunking.ipynb
│   ├── 03_explorar_aneel.ipynb
│   └── 04_test_embeddings.ipynb
│
├── src/
│   ├── agents/
│   │   ├── graph.py               # Orquestrador / roteador central
│   │   ├── operations_agent.py    # Agente de dados operacionais (Text-to-SQL)
│   │   ├── rag_agent.py           # Agente RAG simples (busca híbrida)
│   │   └── regulatory_agent.py    # Agente regulatório (Qdrant + Reranker)
│   │
│   ├── app/
│   │   ├── app.py                 # Ponto de entrada Streamlit
│   │   ├── chat_tab.py            # Aba de chat
│   │   └── dashboard_tab.py       # Aba de dashboard de indicadores
│   │
│   ├── ingestion/
│   │   ├── chunking.py            # Fatiamento dos textos extraídos
│   │   ├── extract_pdf.py         # Extração de texto dos PDFs PRODIST
│   │   └── load_aneel.py          # Tratamento do CSV da ANEEL
│   │
│   ├── reranking/
│   │   └── rerank.py              # Cross-Encoder para reordenação
│   │
│   └── vectorstore/
│       ├── embed.py               # Geração de embeddings + indexação Qdrant/BM25
│       └── hybrid_search.py       # Retriever híbrido (Dense + BM25 + RRF)
│
└── tests/
    ├── test_agents.py
    ├── test_ingestion.py
    └── test_reranking.py
```

### Descrição dos módulos

| Diretório | Responsabilidade |
|---|---|
| `src/agents/` | Agentes LLM (RAG, regulatório, operacional) orquestrados por um grafo (`graph.py`) |
| `src/app/` | Interface Streamlit com abas de chat e dashboard |
| `src/ingestion/` | Pipeline de ingestão: extração de PDF, chunking e carga dos dados ANEEL |
| `src/reranking/` | Reranking dos resultados de busca com Cross-Encoder |
| `src/vectorstore/` | Geração de embeddings e busca híbrida (BM25 + vetorial) |
| `data/raw/` | PDFs dos módulos PRODIST e CSV bruto da ANEEL |
| `data/processed/` | Dados processados e prontos para uso (parquet, chunks) |
| `docker/` | Containerização da aplicação (Qdrant + App) |
| `notebooks/` | Exploração e testes de componentes do pipeline |
| `tests/` | Testes automatizados com Pytest |

---

## ✅ Pré-requisitos

- Python 3.11+
- [Docker](https://www.docker.com/) e Docker Compose (obrigatório)
- Uma **API Key do Google Gemini** (obtida gratuitamente em [aistudio.google.com](https://aistudio.google.com/))
- (Opcional) GPU com CUDA para acelerar a geração de embeddings

---

## Instalação Local

### 1. Clone o repositório

```bash
git clone https://github.com/Portfolio-profissional-vinii/utilities-copilot
cd utilities-copilot
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GOOGLE_API_KEY=sua_chave_gemini_aqui
QDRANT_URL=http://localhost:6333
```

> A `GOOGLE_API_KEY` também pode ser inserida diretamente na barra lateral da interface Streamlit em tempo de execução.

### 5. Suba o Qdrant (banco vetorial)

```bash
docker compose -f docker/docker-compose.yml up qdrant -d
```

---

## Pipeline de Dados (Ingestão)

Antes de usar o Copilot pela primeira vez, é necessário processar os dados brutos. Coloque:

- Os PDFs dos módulos PRODIST em `data/raw/prodist/`
- O CSV de indicadores da ANEEL em `data/raw/aneel/`

Execute o pipeline na seguinte ordem:

```bash
# 1. Extrai texto dos PDFs do PRODIST
python -m src.ingestion.extract_pdf

# 2. Fatia o texto extraído em chunks
python -m src.ingestion.chunking

# 3. Trata e converte o CSV da ANEEL para Parquet
python -m src.ingestion.load_aneel

# 4. Gera embeddings, indexa no Qdrant e constrói o índice BM25
python -m src.vectorstore.embed
```

Ao final, você terá:
- Vetores densos indexados na coleção `prodist_normativas` no Qdrant
- Um índice BM25 salvo em `data/vectorstore/bm25.pkl`
- Um Parquet de indicadores em `data/processed/aneel_indicadores.parquet`

---

## ▶️ Executando a Aplicação

### Localmente (Streamlit)

```bash
streamlit run src/app/app.py
```

Acesse `http://localhost:8501`, informe sua Gemini API Key na barra lateral e comece a conversar.

### Via Docker Compose (App + Qdrant)

```bash
docker compose -f docker/docker-compose.yml up --build
```

Isso sobe dois serviços:
- `qdrant`: banco vetorial (portas `6333`/`6334`)
- `copilot-app`: aplicação Streamlit (porta `8501`)

> ⚠️ **Nota sobre deploy em nuvem:** este projeto foi testado para deploy gratuito em algumas plataformas, porém, devido ao tamanho das dependências (PyTorch, sentence-transformers, Qdrant, modelos de reranking, etc.), planos gratuitos costumam não ter recursos suficientes (RAM/CPU/armazenamento) para rodá-lo de forma estável. **Localmente e em planos pagos com mais recursos, a aplicação roda sem problemas.**

---

## Como Usar

1. **Aba de Chat** — digite perguntas em linguagem natural sobre:
   - Normativas do PRODIST (ex: *"Quais as regras de proteção para subestações de MT?"*)
   - Indicadores operacionais da ANEEL (ex: *"Qual a média do DEC em 2020?"*)

   O roteador identifica automaticamente a intenção e aciona o agente correto, sempre citando a fonte (**Módulo** e **Página**) quando a resposta é regulatória.

2. **Aba de Dashboard** — explore visualmente os indicadores da ANEEL, com filtros por distribuidora, indicador e ano, gráficos de evolução temporal, comparação entre indicadores e estatísticas descritivas (mínimo, máximo, mediana, desvio padrão).

---

## Testes

O projeto conta com testes automatizados via **Pytest**:

```bash
pytest
```

Os testes cobrem:
- `test_ingestion.py` — validação da existência dos dados processados
- `test_agents.py` — validação de consultas ao DuckDB
- `test_reranking.py` — validação da ordenação correta do Cross-Encoder

---

## 🔐 Segurança e Boas Práticas

- Nunca versione o arquivo `.env` (já incluído no `.gitignore` e `.dockerignore`)
- As pastas `data/raw/`, `data/processed/` e `qdrant_storage/` também são ignoradas por padrão, pois contêm dados potencialmente sensíveis/pesados
- A API Key do Gemini pode ser fornecida em tempo de execução via interface, evitando hardcode no código

---

## Roadmap / Possíveis Melhorias

- [ ] Cache de respostas para perguntas recorrentes
- [ ] Suporte a múltiplos LLMs (fallback entre provedores)
- [ ] Streaming de respostas na interface de chat
- [ ] Avaliação automatizada de qualidade do RAG (ex: RAGAS)
- [ ] Autenticação de usuários na interface Streamlit
- [ ] Exportação de relatórios do dashboard em PDF/Excel

---

## 📄 Licença

Este projeto está licenciado sob a **[MIT License](https://opensource.org/licenses/MIT)**.

Foi desenvolvido para fins de **aprendizado e portfólio**, sendo livre para uso, cópia, modificação e estudo, desde que mantidos os devidos créditos.

> **Nota sobre os dados utilizados:** os dados de indicadores de continuidade e os módulos normativos do PRODIST utilizados neste projeto são **dados públicos**, disponibilizados pela [ANEEL](https://www.gov.br/aneel/) sob a Lei de Acesso à Informação (Lei nº 12.527/2011). Esses dados **não são cobertos pela licença MIT do código** — pertencem à ANEEL e devem ser citados como fonte em qualquer uso derivado.
