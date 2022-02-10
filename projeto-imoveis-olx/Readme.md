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
1. Altere algumas variáveis do arquivo airflow.cfg, de forma que elas façam sentido com o seu diretório. Variáveis, tais como: dags_folder, plugins_folder, base_log_folder, dag_processor_manager_log_location, child_process_log_directory. Ou, se preferir, coloque o arquivo da DAG e a pasta com os scripts de extração (presentes em data_extraction/spiders) no seu diretório do Airflow.
2. De qualquer forma, altere os bash_commands na DAG para que faça sentido com o seu diretório.
3. Analogamente, altere o parâmetro FEED_URI no método CrawlerProcess das spiders para que faça sentido com o seu diretório. Esse parâmetro deve ter o caminho da pasta onde os arquivos extraídos devem ser armazenados.
4. Para usar o executor LocalExecutor, da forma que está no airflow.cfg, é necessário usar o Postgresql. Para isso, no terminal do SQL (supondo que você tenha o Postgresql):
```
CREATE USER airflow PASSWORD 'airflow';
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
```
Os valores de usuário, senha e nome do database podem ser de sua escolha, mas será necessário mudar o valor da variável sql_alchemy_conn no airflow.cfg, caso seja diferente dos aqui propostos.

5. Caso queira usar o executor SequentialExecutor, é só alterar a variável de LocalExecutor para SequentialExecutor e descomentar a variável sql_alchemy_conn que está comentada e comentar a que não está comentada no airflow.cfg. Com isso, será usado o sqlite.
6. Após tudo isso, inicialize o airflow:
```
airflow db init
airflow webserver -p 8080
airflow scheduler
```
7. Inicializado o airflow, acesse ```localhost:8080``` e rode a DAG.
