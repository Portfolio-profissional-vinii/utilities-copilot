import streamlit as st
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PARQUET_PATH = ROOT_DIR / "data" / "processed" / "aneel_indicadores.parquet"

def render_dashboard_tab():
    st.subheader("📊 Dashboard Operacional ANEEL")
    
    if not PARQUET_PATH.exists():
        st.warning("Base de dados processada não encontrada. Execute a ingestão do CSV primeiro.")
        return

    df = pd.read_parquet(PARQUET_PATH)

    st.markdown("### Visão Geral dos Indicadores")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Registros", f"{len(df):,}")
    col2.metric("Distribuidoras", df['SigAgente'].nunique() if 'SigAgente' in df.columns else "N/A")
    col3.metric("Indicadores Mapeados", df['SigIndicador'].nunique() if 'SigIndicador' in df.columns else "N/A")

    st.divider()

    # Filtros interativos
    if 'SigAgente' in df.columns and 'SigIndicador' in df.columns:
        agente = st.selectbox("Selecione a Distribuidora (SigAgente):", options=df['SigAgente'].unique())
        indicador = st.selectbox("Selecione o Indicador:", options=df['SigIndicador'].unique())

        df_filtrado = df[(df['SigAgente'] == agente) & (df['SigIndicador'] == indicador)]

        if not df_filtrado.empty and 'AnoIndice' in df_filtrado.columns and 'VlrIndiceEnviado' in df_filtrado.columns:
            st.markdown(f"**Evolução do indicador {indicador} - {agente}**")
            chart_data = df_filtrado.groupby('AnoIndice')['VlrIndiceEnviado'].mean().reset_index()
            st.line_chart(chart_data, x='AnoIndice', y='VlrIndiceEnviado')
            
            st.dataframe(df_filtrado.head(20), use_container_width=True)