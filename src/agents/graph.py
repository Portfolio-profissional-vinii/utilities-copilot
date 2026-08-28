import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Garante acesso à raiz do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

from src.agents.regulatory_agent import iniciar_copilot
from src.agents.operations_agent import consultar_dados_operacionais

class CopilotOrchestrator:
    def __init__(self):
        # Modelo roteador com baixa temperatura para decisão determinística
        self.router_llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
        
        # Agente Regulatório (RAG / Qdrant)
        self.regulatory_agent = iniciar_copilot()
        
        # Prompt para classificação de intenção
        self.router_prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é o roteador central do sistema Copilot Total Utiliti.
Dada a pergunta do usuário, classifique a intenção em exatamente uma das categorias abaixo:

- OPERACIONAL: Perguntas sobre números, estatísticas, indicadores (DEC, FEC), valores apurados por distribuidoras (CEA, EAC, ETO, etc.), médias ou dados históricos de continuidade.
- REGULATORIO: Perguntas sobre leis, normativas, PRODIST, regulação da ANEEL, regras de faturamento, ressarcimento, medição ou termos técnicos regulatórios.

Responda APENAS com uma palavra: 'OPERACIONAL' ou 'REGULATORIO'."""),
            ("user", "{pergunta}")
        ])
        
        self.router_chain = self.router_prompt | self.router_llm | StrOutputParser()

    def responder(self, pergunta: str) -> str:
        # 1. Classifica a pergunta
        categoria = self.router_chain.invoke({"pergunta": pergunta}).strip().upper()
        
        # 2. Roteia para o agente adequado
        if "OPERACIONAL" in categoria:
            return self.consultar_operacional(pergunta)
        else:
            return self.consultar_regulatorio(pergunta)

    def consultar_operacional(self, pergunta: str) -> str:
        return consultar_dados_operacionais(pergunta)

    def consultar_regulatorio(self, pergunta: str) -> str:
        return self.regulatory_agent.invoke(pergunta)

if __name__ == "__main__":
    orchestrator = CopilotOrchestrator()
    
    print("--- Teste 1: Dúvida Operacional ---")
    p1 = "Qual foi o valor médio do DEC em 2020?"
    print(f"Pergunta: {p1}")
    print(f"Resposta:\n{orchestrator.responder(p1)}\n")

    print("--- Teste 2: Dúvida Regulatória ---")
    p2 = "O que dizem as regras sobre ressarcimento por danos elétricos?"
    print(f"Pergunta: {p2}")
    print(f"Resposta:\n{orchestrator.responder(p2)}\n")