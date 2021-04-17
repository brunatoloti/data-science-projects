# Projeto Imóveis OLX

Repositório com os arquivos de projeto pessoal, onde:
- Extraio uma amostra de dados de anúncios de imóveis do site OLX.
- Faço uma análise exploratória e visualização da amostra de dados extraída. **(EM ANDAMENTO)**

**Pastas**
<b></b>
- Na pasta **data_extraction**, estão presentes os arquivos referentes ao crawler da amostra de anúncios de imóveis a venda e para alugar do site OLX. O web scraping foi feito usando a biblioteca **Scrapy**.
- Na pasta **data_exploration_and_visualization**, está presente o notebook com as análises exploratórias e as visualizações dos dados extraídos. **(EM ANDAMENTO)**

**Uso - Extração de Dados**
<b></b>
1. Instale os requirements na sua máquina ou no seu ambiente virtua;
2. Percorra o caminho até a pasta **spiders** e rode:
```
scrapy crawl ads -o <nome-do-arquivo>.<extensão-do-arquivo>
```
