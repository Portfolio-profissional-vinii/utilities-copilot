"""
Testes da Etapa 2 (vector store / busca híbrida).

Sugestões de casos a testar:
- embed: chunks indexados são recuperáveis por uma busca simples
- hybrid_search: uma query por palavra-chave exata (ex: "Art. 178")
  retorna o chunk correto mesmo se a similaridade vetorial for baixa
- hybrid_search: uma query conceitual retorna chunks semanticamente
  relacionados, mesmo sem sobreposição exata de palavras
"""
