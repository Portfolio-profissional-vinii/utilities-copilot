import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

from src.reranking.rerank import Reranker

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "prodist_normativas"

def formatar_docs(docs):
    texto_formatado = []

    for i, doc in enumerate(docs, 1):
        documento = doc.metadata.get("documentos", "Documento não identificado")
        modulo = doc.metadata.get("modulo", "Módulo não identificado")
        pagina = doc.metadata.get("pagina", "Página não identificada")

        texto_formatado.append(
            f"--- FONTE {i} ---\n"
            f"Documento: {documento}\n"
            f"Módulo: {modulo}\n"
            f"Página: {pagina}\n"
            f"Texto:\n{doc.page_content}"
        )

    return "\n\n".join(texto_formatado)

def iniciar_copilot():
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
    client = QdrantClient(url=QDRANT_URL)
    
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )
    
    # 1. Busca vetorial mais ampla no Qdrant (top 15)
    retriever = vector_store.as_retriever(search_kwargs={"k": 15})
    
    # 2. Instancia o Re-ranker
    reranker = Reranker()
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

    system_prompt = (
    "Você é o Copilot Regulatório da Total Utiliti, especialista em normas da ANEEL e PRODIST.\n\n"

    "Responda à dúvida do usuário EXCLUSIVAMENTE com base no contexto fornecido.\n\n"

    "REGRAS OBRIGATÓRIAS:\n"
    "1. Não invente informações, valores, artigos, módulos ou páginas.\n"
    "2. Cada informação apresentada deve ser fundamentada em uma fonte do contexto.\n"
    "3. Cite a fonte no formato [Módulo X, Página Y].\n"
    "4. Use exatamente o módulo e a página informados na fonte correspondente.\n"
    "5. Se a página não estiver disponível, use [Página não identificada].\n"
    "6. Nunca escreva 'Página N/A' se a página estiver disponível no contexto.\n"
    "7. Não crie links, HTML, SVG ou referências como [svg](...).\n"
    "8. Se a informação não estiver no contexto, diga que não encontrou essa informação "
    "nas normativas fornecidas.\n\n"

    "Contexto:\n{context}"
)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{question}")
    ])

    def buscar_e_reordenar(pergunta: str):
        # Recupera candidatos do Qdrant
        docs_brutos = retriever.invoke(pergunta)
        # Reordena e seleciona os 5 mais relevantes
        docs_filtrados = reranker.rerank(pergunta, docs_brutos, top_n=5)
        return formatar_docs(docs_filtrados)

    # Cadeia RAG com Re-ranking integrado
    chain = (
        {"context": buscar_e_reordenar, "question": lambda x: x}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain