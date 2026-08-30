EVAL_SET = [
    {
        "pergunta": "Quais os requisitos de proteção para subestações de MT e AT?",
        "categoria_esperada": "REGULATORIO",
        "modulo_esperado": "Módulo 3",
        "pagina_esperada": 15,
    },
    {
        "pergunta": "Qual o prazo para a distribuidora responder a um pedido de ressarcimento por danos elétricos?",
        "categoria_esperada": "REGULATORIO",
        "modulo_esperado": "Módulo 9",
        "pagina_esperada": None, 
    },
    {
        "pergunta": "O que caracteriza uma interrupção de curta duração no fornecimento de energia?",
        "categoria_esperada": "REGULATORIO",
        "modulo_esperado": "Módulo 8",
        "pagina_esperada": None,
    },
    {
        "pergunta": "Quais são as regras de aterramento exigidas para unidades consumidoras?",
        "categoria_esperada": "REGULATORIO",
        "modulo_esperado": "Módulo 3",
        "pagina_esperada": None,
    },
    {
        "pergunta": "Como é calculado o indicador DIC?",
        "categoria_esperada": "REGULATORIO",
        "modulo_esperado": "Módulo 8",
        "pagina_esperada": None,
    },

    {
        "pergunta": "Qual foi o valor médio do indicador DEC em 2020?",
        "categoria_esperada": "OPERACIONAL",
        "sql_esperado_contem": ["AVG", "DEC", "2020"],
    },
    {
        "pergunta": "Qual distribuidora teve o maior valor de FEC em 2021?",
        "categoria_esperada": "OPERACIONAL",
        "sql_esperado_contem": ["MAX", "FEC", "2021", "ORDER BY"],
    },
    {
        "pergunta": "Quantos registros existem para a distribuidora CEA?",
        "categoria_esperada": "OPERACIONAL",
        "sql_esperado_contem": ["COUNT", "CEA"],
    },
    {
        "pergunta": "Qual a média de DECXNC por ano entre 2020 e 2023?",
        "categoria_esperada": "OPERACIONAL",
        "sql_esperado_contem": ["AVG", "DECXNC", "GROUP BY"],
    },

    {
        "pergunta": "O indicador DEC tem alguma regra específica de cálculo definida no PRODIST?",
        "categoria_esperada": "REGULATORIO", 
        "pagina_esperada": None,
    },
    {
        "pergunta": "me fala sobre proteção de subestação",
        "categoria_esperada": "REGULATORIO",
        "modulo_esperado": "Módulo 3",
        "pagina_esperada": None,
    },
    {
        "pergunta": "quanto foi o dec da eac",
        "categoria_esperada": "OPERACIONAL",
        "sql_esperado_contem": ["DEC", "EAC"],
    },
]