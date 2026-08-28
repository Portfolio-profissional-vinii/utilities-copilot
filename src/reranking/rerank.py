import os
import sys
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

# Modelo de Cross-Encoder multilíngue e de alta precisão
MODEL_NAME = "BAAI/bge-reranker-base"

class Reranker:
    def __init__(self, model_name: str = MODEL_NAME):
        # Carrega o modelo de re-ranking
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, docs: List[Document], top_n: int = 5) -> List[Document]:
        """
        Recebe a pergunta e uma lista de Documentos do LangChain,
        calcula a pontuação de relevância real e retorna os top_n melhores.
        """
        if not docs:
            return []

        # Prepara os pares (pergunta, conteúdo do documento)
        pairs = [[query, doc.page_content] for doc in docs]
        
        # Calcula os scores do Cross-Encoder
        scores = self.model.predict(pairs)

        # Associa cada documento ao seu novo score
        for doc, score in zip(docs, scores):
            doc.metadata["rerank_score"] = float(score)

        # Ordena em ordem decrescente de pontuação
        sorted_docs = sorted(docs, key=lambda x: x.metadata["rerank_score"], reverse=True)

        return sorted_docs[:top_n]

if __name__ == "__main__":
    # Teste isolado do Reranker
    reranker = Reranker()
    
    pergunta_exemplo = "Qual o prazo para ressarcimento de danos elétricos?"
    docs_ficticios = [
        Document(page_content="O prazo para análise da solicitação de ressarcimento é de 15 dias úteis.", metadata={"source": "Modulo 9"}),
        Document(page_content="O indicador DEC mede a duração equivalente de interrupção por unidade consumidora.", metadata={"source": "Modulo 8"}),
        Document(page_content="A distribuidora deve deferir ou indeferir o pedido em até 15 dias corridos.", metadata={"source": "Modulo 9"}),
    ]

    docs_ranqueados = reranker.rerank(pergunta_exemplo, docs_ficticios, top_n=2)
    
    print("📌 Resultado do Re-ranking:")
    for i, doc in enumerate(docs_ranqueados, 1):
        print(f"{i}. Score: {doc.metadata['rerank_score']:.4f} | Trecho: {doc.page_content}")