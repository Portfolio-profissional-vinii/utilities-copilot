from src.reranking.rerank import Reranker
from langchain_core.documents import Document

def test_reranker_ordenacao():
    reranker = Reranker()
    docs = [
        Document(page_content="O indicador DEC mede a duração da interrupção."),
        Document(page_content="O prazo para ressarcimento de danos é de 15 dias.")
    ]
    resultado = reranker.rerank("qual o prazo de ressarcimento?", docs, top_n=1)
    
    assert len(resultado) == 1
    assert "15 dias" in resultado[0].page_content