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

3. Inicializado o airflow, acesse ```localhost:8080```.
4. Rode a DAG.
