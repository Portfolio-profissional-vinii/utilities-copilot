import json
import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

def carregar_json(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_chunks(chunks, caminho_saida):
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)
    print(f"Chunks salvos em: {caminho_saida}")

def processar_fatiamento(caminho_entrada, caminho_saida, nome_documento):
    dados_paginas = carregar_json(caminho_entrada)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks_finais = []

    for item in dados_paginas:
        pagina_num = item["pagina"]
        texto_pagina = item["texto"]

        pedacos = text_splitter.split_text(texto_pagina)

        for pedaco in pedacos:
            chunks_finais.append({
                "texto": pedaco,
                "metadados": {
                    "documentos": nome_documento,
                    "pagina": pagina_num
                }
            })

        salvar_chunks(chunks_finais, caminho_saida)
        print(f"{nome_documento}: Gerados {len(chunks_finais)} chunks a partir de {len(dados_paginas)} páginas.")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    pasta_processados = BASE_DIR / "data" / "processed"

    arquivo_json = list(pasta_processados.glob("*_extraido.json"))

    if not arquivo_json:
        print("Nenhum arquivo JSON encontrado para fatiar.")
    else:
        print("Iniciando o processo de Chunking...\n")
        for caminho_json in arquivo_json:
            nome_base = caminho_json.stem.replace("_extraido", "")
            caminho_saida = pasta_processados / f"{nome_base}_chunks.json"

            processar_fatiamento(str(caminho_json), str(caminho_saida), nome_documento=nome_base)
            print("-" * 40)