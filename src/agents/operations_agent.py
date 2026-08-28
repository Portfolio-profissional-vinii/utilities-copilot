import os
import sys
import duckdb
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Carrega as variáveis de ambiente do arquivo .env
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

PARQUET_PATH = ROOT_DIR / "data" / "processed" / "aneel_indicadores.parquet"

def executar_query_sql(sql_query: str) -> str:
    """Executa consultas SQL via DuckDB no arquivo Parquet limpo."""
    try:
        con = duckdb.connect()
        con.execute(f"CREATE VIEW indicadores AS SELECT * FROM '{PARQUET_PATH}'")
        df_resultado = con.execute(sql_query).df()
        con.close()
        
        if df_resultado.empty:
            return "Nenhum resultado encontrado para os filtros informados."
        return df_resultado.to_string(index=False)
    except Exception as e:
        return f"Erro ao executar consulta na base de dados: {e}"

def consultar_dados_operacionais(pergunta_usuario: str) -> str:
    """Traduz a dúvida do usuário em SQL, consulta a base e formula a resposta final."""
    
    # Configuração do modelo gemini-3.6-flash
    llm_sql = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
    
    prompt_sql = ChatPromptTemplate.from_messages([
        ("system", """Você é um especialista em SQL para DuckDB. Sua tarefa é converter a pergunta do usuário em uma instrução SQL válida.
        
Tabela disponível: `indicadores`
Colunas da tabela:
- SigAgente (TEXT): Sigla da distribuidora (ex: 'EAC', 'CEA', 'ETO', 'EQUATORIAL')
- SigIndicador (TEXT): Nome do indicador (ex: 'DEC', 'FEC', 'DECXNC', 'FECIPC')
- DscConjUndConsumidoras (TEXT): Nome do conjunto de unidades consumidoras
- AnoIndice (BIGINT): Ano de referência do indicador (ex: 2020)
- NumPeriodoIndice (BIGINT): Mês ou período do indicador (1 a 12)
- VlrIndiceEnviado (DOUBLE): Valor numérico apurado

Regras Importantes:
1. Retorne APENAS o código SQL puro (sem tags de código Markdown como ```sql).
2. Use ILIKE para buscas de texto flexíveis (ex: SigAgente ILIKE '%CEA%').
3. Selecione apenas as colunas relevantes ou agregados (SUM, AVG, COUNT, MAX, MIN)."""),
        ("user", "{pergunta}")
    ])

    cadeia_sql = prompt_sql | llm_sql | StrOutputParser()
    
    query_gerada = cadeia_sql.invoke({"pergunta": pergunta_usuario}).strip()
    query_gerada = query_gerada.replace("```sql", "").replace("```", "").strip()

    resultado_dados = executar_query_sql(query_gerada)

    llm_resposta = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.2)
    
    prompt_resposta = ChatPromptTemplate.from_messages([
        ("system", "Você é o Copilot Operacional da Total Utiliti. Responda a dúvida do usuário de forma clara e direta com base EXCLUSIVAMENTE nos dados tabulares retornados pela consulta SQL."),
        ("user", "Pergunta do Usuário: {pergunta}\n\nDados Encontrados:\n{dados}\n\nResposta:")
    ])

    cadeia_resposta = prompt_resposta | llm_resposta | StrOutputParser()
    return cadeia_resposta.invoke({"pergunta": pergunta_usuario, "dados": resultado_dados})

if __name__ == "__main__":
    pergunta_teste = "Qual foi o valor médio do indicador DEC no ano de 2020?"
    print(f"❓ Pergunta: {pergunta_teste}\n")
    resposta = consultar_dados_operacionais(pergunta_teste)
    print(f"🤖 Copilot Operacional:\n{resposta}")