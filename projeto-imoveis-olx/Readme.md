# Projeto Imóveis OLX

Repositório com os arquivos de projeto pessoal, onde:
- É extraída uma amostra de dados de anúncios de imóveis do site OLX, usando a biblioteca Scrapy e o Airflow.
- É feita uma análise exploratória e visualização da amostra de dados extraída. **(EM ANDAMENTO)**

**Pastas**
<b></b>
- Na pasta **airflow**, estão presentes os arquivos e pastas referentes ao airflow.
- Na pasta **data_extraction**, estão presentes os arquivos referentes ao crawler da amostra de anúncios de imóveis a venda e para alugar do site OLX. O web scraping foi feito usando a biblioteca **Scrapy**. E para o gerenciamento das execuções, foi usado o **Airflow**.
- Na pasta **data_exploration_and_visualization**, está presente o notebook com as análises exploratórias e as visualizações dos dados extraídos. **(EM ANDAMENTO)**

**Uso - Extração de Dados**
<b></b>

1. Vá até a pasta /projeto-imoveis-olx:
```
cd projeto-imoveis-olx
```

2. Como é utilizado o docker:
```
docker build -t projeto-imoveis-olx .
```
```
docker-compose build
```
```
docker-compose up
```

3. Como ao fazer o docker-compose up o postgres estará rodando, em outra janela do terminal acesso o banco que será onde vamos armazenar os dados coletados:
```
docker exec -it postgres  bash
```
```
psql -U airflow
```

4. Crie a tabela imoveisolx no banco, com as colunas id,categoria,tipo,quartos,banheiros,vagas_garagem,detalhes_imovel,detalhes_condominio,cep,cidade,estado,bairro,preco,url,created_at, que são as informações que pegamos do site.
OBS.: id é um serial primary key e created_at é timestamp default now().
5. Inicializado o airflow, acesse ```localhost:8080```.
6. Rode a DAG. Os dados serão inseridos nessa tabela criada.
