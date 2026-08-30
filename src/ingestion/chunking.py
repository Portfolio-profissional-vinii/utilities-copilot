import json
import os
import re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


def carregar_json(caminho_arquivo: str) -> list:
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)


def salvar_chunks(chunks: list, caminho_saida: str) -> None:
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)
    print(f"Chunks salvos em: {caminho_saida}")


def extrair_modulo(nome_documento: str) -> str:
    match = re.search(r'modulo[_\s]?(\d+)', nome_documento, re.IGNORECASE)
    if match:
        return f"Módulo {match.group(1)}"

    if re.search(r'resolucao[-_]normativa[-_]?1000', nome_documento, re.IGNORECASE):
        return "REN 1000/2021"

    print(f"AVISO: não foi possível extrair módulo de '{nome_documento}' — usando nome bruto.")
    return nome_documento

def processar_fatiamento(caminho_entrada: str, caminho_saida: str, nome_documento: str) -> None:
    dados_paginas = carregar_json(caminho_entrada)
    modulo = extrair_modulo(nome_documento)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len,
        separators=[
            "\n\n",
            "\nArt.",
            "\n§",
            "\nSeção",
            "\nSEÇÃO",
            "\nCAPÍTULO",
            "\nCapítulo",
            "\nSUBSEÇÃO",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks_finais = []

    for item in dados_paginas:
        pagina_num = item["pagina"]
        texto_pagina = item["texto"]

        pedacos = text_splitter.split_text(texto_pagina)

        for pedaco in pedacos:
            pedaco = pedaco.strip()
            if pedaco:  # ignora chunks vazios
                chunks_finais.append({
                    "texto": pedaco,
                    "metadados": {
                        "documentos": nome_documento,
                        "modulo": modulo,
                        "pagina": pagina_num
                    }
                })

    salvar_chunks(chunks_finais, caminho_saida)
    print(f"{nome_documento}: Gerados {len(chunks_finais)} chunks de {len(dados_paginas)} páginas.")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    pasta_processados = BASE_DIR / "data" / "processed"

    arquivo_json = list(pasta_processados.glob("*_extraido.json"))

    if not arquivo_json:
        print("Nenhum arquivo JSON encontrado para fatiar.")
    else:
        print("Iniciando o processo de Chunking...\n")
        for caminho_json in sorted(arquivo_json):
            nome_base = caminho_json.stem.replace("_extraido", "")
            caminho_saida = pasta_processados / f"{nome_base}_chunks.json"

            processar_fatiamento(str(caminho_json), str(caminho_saida), nome_documento=nome_base)
            print("-" * 40)