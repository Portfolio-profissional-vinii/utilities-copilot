import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.vectorstore.hybrid_search import configurar_buscador

load_dotenv()

def iniciar_copilot():
    llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

    retriever = configurar_buscador(k_resultados=8)

    template = """Você é um assistente especialista nas normativas da ANEEL (PRODIST).
    Sua missão é responder à pergunta do usuário baseando-se ÚNICA E EXCLUSIVAMENTE no contexto fornecido abaixo.
    Sempre que possível, cite a fonte (Módulo e Página) da onde retirou a resposta.
    Se a resposta não estiver no contexto, diga claramente: "Não encontrei essa informação nas normativas fornecidas".
    Não invente leis ou regras. Seja claro, profissional e direto.

    Contexto das Normativas:
    {context}

    Pergunta do Usuário: {question}

    Resposta:"""
    
    prompt = PromptTemplate.from_template(template)

    def formatar_documentos(docs):
        # Formata o conteúdo do chunk precedido pelos seus metadados
        textos = []
        for doc in docs:
            modulo = doc.metadata.get('modulo', 'Módulo Desconhecido')
            pagina = doc.metadata.get('pagina', 'N/A')
            textos.append(f"[Fonte: {modulo}, Página: {pagina}]\n{doc.page_content}")
        return "\n\n".join(textos)

    rag_chain = (
        {"context": retriever | formatar_documentos, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

if __name__ == "__main__":
    print("Ligando o motor de busca híbrida (Dense + BM25 com RRF)...")
    try:
        agente = iniciar_copilot()
        print("\nCopilot ANEEL iniciado! Digite 'sair' para encerrar.")
        try:
            pergunta = input("\nVocê: ")
        except EOFError:
            sys.exit(0)
            
        if pergunta.strip().lower() in ['sair', 'exit', 'quit'] or not pergunta.strip():
            sys.exit(0)
            
        print("Pesquisando nas leis e formulando a resposta...\n")
        resposta = agente.invoke(pergunta)
        
        print("Copilot Total Utiliti:")
        print(resposta)
            
    except Exception as e:
        print(f"Erro ao inicializar o assistente: {e}")