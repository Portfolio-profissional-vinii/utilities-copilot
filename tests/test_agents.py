from src.agents.operations_agent import executar_query_sql

def test_consulta_duckdb():
    resultado = executar_query_sql("SELECT COUNT(*) FROM indicadores")
    assert "Nenhum resultado" not in resultado