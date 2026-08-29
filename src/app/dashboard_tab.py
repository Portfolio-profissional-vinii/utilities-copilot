import streamlit as st
import pandas as pd
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PARQUET_PATH = ROOT_DIR / "data" / "processed" / "aneel_indicadores.parquet"


def formatar_valor(valor):
    if pd.isna(valor):
        return "—"

    if abs(valor) < 1:
        percentual = valor * 100

        if percentual.is_integer():
            return f"{int(percentual)}%"

        return f"{percentual:.2f}%"

    if float(valor).is_integer():
        return f"{int(valor):,}".replace(",", ".")

    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render_dashboard_tab():

    if not PARQUET_PATH.exists():
        st.error("Base de indicadores não encontrada.")
        return

    try:
        df = pd.read_parquet(PARQUET_PATH)
    except Exception as e:
        st.error(f"Erro ao carregar os indicadores: {e}")
        return

    if df.empty:
        st.warning("A base de indicadores está vazia.")
        return

    if "SigAgente" in df.columns:
        df["SigAgente"] = df["SigAgente"].fillna("Não informado")

    if "SigIndicador" in df.columns:
        df["SigIndicador"] = df["SigIndicador"].fillna("Não informado")

    if "VlrIndiceEnviado" in df.columns:
        df["VlrIndiceEnviado"] = pd.to_numeric(
            df["VlrIndiceEnviado"],
            errors="coerce",
        )

    if "AnoIndice" in df.columns:
        df["AnoIndice"] = pd.to_numeric(
            df["AnoIndice"],
            errors="coerce",
        )

    st.markdown(
        """
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:20px;
        ">
            <div>
                <h1 style="
                    margin:0;
                    font-size:30px;
                    font-weight:700;
                ">
                    📊 Indicadores ANEEL
                </h1>
                <p style="
                    margin:5px 0 0 0;
                    color:#8b949e;
                    font-size:14px;
                ">
                    Monitoramento dos indicadores operacionais
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pergunta = st.text_input(
        "Pesquisar",
        placeholder="🔎  Buscar distribuidora ou indicador...",
        label_visibility="collapsed",
    )

    if pergunta.strip():

        termo = pergunta.strip().lower()

        mask = pd.Series(False, index=df.index)

        for coluna in ["SigIndicador", "SigAgente"]:

            if coluna in df.columns:

                mask |= (
                    df[coluna]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        termo,
                        na=False,
                        regex=False,
                    )
                )

        df_busca = df[mask].copy()

    else:
        df_busca = df.copy()

    col1, col2, col3 = st.columns([1.5, 1.5, 1])

    if "SigAgente" in df_busca.columns:

        agentes = sorted(
            df_busca["SigAgente"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        agente = col1.selectbox(
            "Distribuidora",
            ["Todas"] + agentes,
        )

    else:
        agente = "Todas"

    df_filtrado = df_busca.copy()

    if agente != "Todas":

        df_filtrado = df_filtrado[
            df_filtrado["SigAgente"] == agente
        ]

    if "SigIndicador" in df_filtrado.columns:

        indicadores = sorted(
            df_filtrado["SigIndicador"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        indicador = col2.selectbox(
            "Indicador",
            ["Todos"] + indicadores,
        )

    else:
        indicador = "Todos"

    if indicador != "Todos":

        df_filtrado = df_filtrado[
            df_filtrado["SigIndicador"] == indicador
        ]

    if "AnoIndice" in df_filtrado.columns:

        anos = sorted(
            df_filtrado["AnoIndice"]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )

        ano = col3.selectbox(
            "Ano",
            ["Todos"] + anos,
        )

        if ano != "Todos":

            df_filtrado = df_filtrado[
                df_filtrado["AnoIndice"] == ano
            ]

    if df_filtrado.empty:

        st.warning("Nenhum dado encontrado.")

        return

    total_registros = len(df_filtrado)

    total_distribuidoras = (
        df_filtrado["SigAgente"].nunique()
        if "SigAgente" in df_filtrado.columns
        else 0
    )

    total_indicadores = (
        df_filtrado["SigIndicador"].nunique()
        if "SigIndicador" in df_filtrado.columns
        else 0
    )

    if "VlrIndiceEnviado" in df_filtrado.columns:

        valores = df_filtrado[
            "VlrIndiceEnviado"
        ].dropna()

        media = valores.mean() if not valores.empty else None

    else:
        valores = pd.Series(dtype=float)
        media = None

    st.markdown("<br>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Registros",
        f"{total_registros:,}".replace(",", "."),
    )

    k2.metric(
        "Distribuidoras",
        f"{total_distribuidoras:,}".replace(",", "."),
    )

    k3.metric(
        "Indicadores",
        f"{total_indicadores:,}".replace(",", "."),
    )

    k4.metric(
        "Média",
        formatar_valor(media),
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if (
        "AnoIndice" in df_filtrado.columns
        and "VlrIndiceEnviado" in df_filtrado.columns
    ):

        chart_df = (
            df_filtrado
            .dropna(
                subset=[
                    "AnoIndice",
                    "VlrIndiceEnviado",
                ]
            )
            .groupby("AnoIndice")[
                "VlrIndiceEnviado"
            ]
            .mean()
            .reset_index()
            .sort_values("AnoIndice")
        )

        if not chart_df.empty:

            chart_df["VlrIndiceEnviado"] *= 100

            chart_df = chart_df.set_index(
                "AnoIndice"
            )

            titulo_indicador = (
                indicador
                if indicador != "Todos"
                else "Indicadores"
            )

            st.markdown(
                f"""
                <div style="
                    margin-bottom:8px;
                    font-size:18px;
                    font-weight:600;
                ">
                    Evolução — {titulo_indicador}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.line_chart(
                chart_df,
                use_container_width=True,
            )

    if (
        "SigIndicador" in df_filtrado.columns
        and "VlrIndiceEnviado" in df_filtrado.columns
        and indicador == "Todos"
    ):

        comparacao = (
            df_filtrado
            .dropna(
                subset=["VlrIndiceEnviado"]
            )
            .groupby("SigIndicador")[
                "VlrIndiceEnviado"
            ]
            .mean()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        if not comparacao.empty:

            comparacao["VlrIndiceEnviado"] *= 100

            comparacao = comparacao.set_index(
                "SigIndicador"
            )

            st.markdown(
                """
                <div style="
                    margin:25px 0 8px 0;
                    font-size:18px;
                    font-weight:600;
                ">
                    Comparação dos indicadores
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.bar_chart(
                comparacao,
                use_container_width=True,
            )

    if not valores.empty:

        st.markdown(
            """
            <div style="
                margin:25px 0 10px 0;
                font-size:18px;
                font-weight:600;
            ">
                Estatísticas
            </div>
            """,
            unsafe_allow_html=True,
        )

        s1, s2, s3, s4 = st.columns(4)

        s1.metric(
            "Mínimo",
            formatar_valor(valores.min()),
        )

        s2.metric(
            "Máximo",
            formatar_valor(valores.max()),
        )

        s3.metric(
            "Mediana",
            formatar_valor(valores.median()),
        )

        s4.metric(
            "Desvio padrão",
            formatar_valor(valores.std()),
        )

    st.markdown(
        """
        <div style="
            margin:25px 0 10px 0;
            font-size:18px;
            font-weight:600;
        ">
            Dados
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabela = df_filtrado.head(100).copy()

    if "VlrIndiceEnviado" in tabela.columns:

        tabela["VlrIndiceEnviado"] = tabela[
            "VlrIndiceEnviado"
        ].apply(formatar_valor)

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
    )