import pymupdf
import re
import os
import json
from pathlib import Path

def limpar_texto(texto_bruto: str) -> str:
    """
    Preserva a estrutura de parágrafos para que o chunker possa usar
    quebras duplas de linha como fronteiras naturais entre seções normativas.
    Remove apenas espaços excessivos dentro de cada linha.
    """
    # Normaliza múltiplas linhas em branco para separador de parágrafo duplo
    texto = re.sub(r'\n{3,}', '\n\n', texto_bruto)
    # Remove espaços e tabs excessivos dentro de cada linha (sem apagar newlines)
    linhas = [re.sub(r'[ \t]{2,}', ' ', linha).strip() for linha in texto.split('\n')]
    resultado = '\n'.join(linhas)
    return resultado.strip()

def extrair_pdf(caminho_pdf):
    print(f"Iniciando extração do arquivo: {caminho_pdf}")

    try:
        doc = pymupdf.open(caminho_pdf)
    except Exception as e:
        print(f" Erro ao abrir o PDF: {e}")
        return[]

    documento_processado = []

    for num_pagina, pagina in enumerate(doc):
        texto_bruto = pagina.get_text()
        if texto_bruto.strip():
            texto_limpo = limpar_texto(texto_bruto)

            documento_processado.append({"pagina": num_pagina + 1,
                                         "texto": texto_limpo})

    print(f"Extração Concluída! {len(documento_processado)} páginas processadas.")
    return documento_processado

def salvar_json(dados, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(dados,f,ensure_ascii=False, indent=4)

    print(f"Arquivo salvo com sucesso em: {caminho_saida}")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    pasta_pdfs = BASE_DIR / "data" / "raw" / "prodist"
    pasta_processados = BASE_DIR / "data" / "processed"

    arquivos_pdf = list(pasta_pdfs.glob("*.pdf"))

    if not arquivos_pdf:
        print(f"Nenhum PDF encontrado na pasta: {pasta_pdfs}")
    else:
        print(f"Encontrados {len(arquivos_pdf)} documentos para processar. \n")

        for pdf_path in arquivos_pdf:
            nome_original = pdf_path.stem
            json_saida = pasta_processados / f"{nome_original}_extraido.json"

            dados_extraidos = extrair_pdf(str(pdf_path))
            if dados_extraidos:
                salvar_json(dados_extraidos, str(json_saida))
            print("-" * 40)
                