# docker/ — Etapa 5 (containerização)

## Objetivo
Empacotar a aplicação inteira (app Streamlit + dependências + vector store,
se aplicável) para rodar de forma reprodutível em qualquer máquina.

## O que implementar aqui (sugestão de arquivos)
- `Dockerfile` — imagem da aplicação Python (Streamlit + agentes)
- `docker-compose.yml` — orquestra o container da app (e o do vector store,
  se ele rodar como serviço separado, como o Qdrant)

## Perguntas para guiar sua implementação
1. Que imagem base faz sentido (`python:3.11-slim`)? O que precisa ser
   instalado além das dependências do `requirements.txt`?
2. Se usar Qdrant como serviço separado (via `docker-compose`), como o app
   se conecta a ele (nome do serviço vs `localhost`)?
3. Como persistir os dados do vector store entre reinícios do container
   (volumes)?
4. Como passar variáveis de ambiente sensíveis (chaves de API) sem
   colocá-las na imagem?
