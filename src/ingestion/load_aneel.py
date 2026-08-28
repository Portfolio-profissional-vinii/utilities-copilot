import pandas as pd
from pathlib import Path

def carregar_e_tratar_aneel():
    # Mapeamento de diretórios do projeto
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    RAW_PATH = ROOT_DIR / "data" / "raw" / "aneel"
    PROCESSED_PATH = ROOT_DIR / "data" / "processed"
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    # Localizar o arquivo CSV na pasta raw
    csv_files = list(RAW_PATH.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("Nenhum arquivo CSV encontrado em data/raw/aneel/")

    arquivo_csv = csv_files[0]
    print(f"📂 Carregando base ANEEL: {arquivo_csv.name}")

    # Leitura lidando com codificação
    try:
        df = pd.read_csv(arquivo_csv, sep=";", encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(arquivo_csv, sep=";", encoding="latin1")

    # Limpeza e conversões numéricas
    if 'VlrIndiceEnviado' in df.columns:
        df['VlrIndiceEnviado'] = (
            df['VlrIndiceEnviado']
            .astype(str)
            .str.replace('.', '', regex=False)  # Remove ponto de milhar se houver
            .str.replace(',', '.', regex=False)  # Converte vírgula decimal para ponto
            .astype(float)
        )

    # Tipagem das colunas numéricas e texto
    df['AnoIndice'] = pd.to_numeric(df['AnoIndice'], errors='coerce')
    df['NumPeriodoIndice'] = pd.to_numeric(df['NumPeriodoIndice'], errors='coerce')

    string_cols = ['SigAgente', 'SigIndicador', 'DscConjUndConsumidoras']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Salva versões limpas em CSV e Parquet para consulta rápida
    output_csv = PROCESSED_PATH / "aneel_indicadores_clean.csv"
    output_parquet = PROCESSED_PATH / "aneel_indicadores.parquet"

    df.to_csv(output_csv, index=False, sep=";")
    df.to_parquet(output_parquet, index=False)

    print(f"✅ Processamento concluído com sucesso!")
    print(f"📊 Registros processados: {len(df)}")
    print(f"💾 Arquivos gerados em {PROCESSED_PATH}")

    return df

if __name__ == "__main__":
    carregar_e_tratar_aneel()