from pathlib import Path

def test_arquivos_processados_existem():
    processed_dir = Path("data/processed")
    assert (processed_dir / "aneel_indicadores.parquet").exists()