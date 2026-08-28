import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
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
    for doc in docs:
        fonte = doc.metadata.get("source", "PRODIST")
        pagina = doc.metadata.get("page", "N/A")
        texto_formatado.append(f"--- Documento: {fonte} (Página {pagina}) ---\n{doc.page_content}")
    return "\n\n".join(texto_formatado)

def iniciar_copilot():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
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
        "Você é o Copilot Regulatório da Total Utiliti, especialista em normas da ANEEL e PRODIST.\n"
        "Responda à dúvida do usuário com base EXCLUSIVAMENTE no contexto fornecido.\n"
        "Se a informação não estiver no contexto, responda que não encontrou essa informação nas normativas fornecidas.\n"
        "Sempre cite a fonte (Módulo e Página) ao final de cada ponto explicado.\n\n"
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