# Projeto Imóveis OLX

#### Objetivo: 
Fazer uma visualização de uma amostra de dados de anúncios de imóveis do site OLX.

#### Ferramentas utilizadas:
- Para a extração e transformação de dados:
    - python
    - airflow
- Para o armazenamento dos dados:
    - postgresql
- Para a visualização de dados:
    - dashboard em shiny (R)
- Para o todo:
    - docker

#### Funcionamento: 
Toda a aplicação roda em um container docker. Container este que possui três serviços:
- airflow: responsável pela parte de extração, transformação e, consequentemente, carregamento dos dados;
- postgresql: responsável pelo armazenamento dos dados;
- shiny: responsável pela visualização dos dados.

#### Detalhes do funcionamento das partes:
- pelo airflow, inicializamos a extração dos dados dos anúncios. Possuímos uma DAG com 1 task por estado brasileiro (para otimizar a extração em relação ao número de anúncios capturados), 1 task dummy e 1 task de limpeza/transformação dos dados.
- basicamente, todas as tasks de extração são levadas para a task dummy que, por sua vez, ao ser executada (depois que todas as tasks de extração finalizam), é levada para a task de transformação. Mais ou menos da forma, por exemplo:
        
        extracao1 >> dummy
        extracao2 >> dummy
        extracao3 >> dummy
        dummy >> limpeza 
- cada task de extração armazena seus dados extraídos na tabela **imoveisolx** que está sendo gerenciada pelo postgresql.
- a task de limpeza/transformação pega os dados dessa tabela **imoveisolx**, faz o tratamento dos dados e armazena os dados limpos e transformados na tabela **imoveisolx_transformed**.
- o serviço do shiny pega esses dados transformados presentes na tabela **imoveisolx_transformed** para gerar os gráficos que aparecerão no shiny dashboard.
- conforme mais dados forem sendo extraídos e, consequentemente, forem entrando no banco de dados, o dashboard vai se atualizando.

#### Uso:
- Como a aplicação roda em um container docker, no terminal digitamos
```
docker-compose up
```
- **Caso seja a primeira vez acessando**, após inicializar o serviço do postgres, precisamos entrar no banco para criar as tabelas **imoveisolx** e **imoveisolx_transformed**. Os códigos de criação dessas tabelas estão na pasta sql aqui deste repositório. Para acessar o banco, em outra aba do terminal:
```
docker exec -it postgres  bash
```
```
psql -U airflow
```
- **OBS.:** Uma vez criadas as tabelas, não é necessário criar novamente. Ou seja, nas próximas vezes que a aplicação for executada, as tabelas já estarão criadas e, caso tenha sido rodado o processo de extração e transformação, as tabelas estarão preenchidas. 
- Com as tabelas já criadas e tendo o airflow pronto para uso, ou seja, já inicializado pelo docker-compose, acessamos
```localhost:8080```
e fazemos o trigger da DAG **crawler-imoveis-olx** de forma que o processo de extração e limpeza dos dados seja iniciado.
- **Caso seja a primeira vez**, deve-se esperar a DAG finalizar a execução para que tenhamos gráficos no dashboard.
- De qualquer forma, tendo o shiny pronto para uso, ou seja, já inicializado pelo docker-compose, acessamos
```localhost:3838```
para vermos o dashboard.

#### Pastas:
- Na pasta **airflow**, estão presentes os arquivos e pastas referentes ao airflow, incluindo o código da DAG.
- Na pasta **data_extraction**, estão presentes os arquivos referentes ao crawler da amostra de anúncios de imóveis da OLX. Ou seja, como o crawler foi feito usando a biblioteca **Scrapy**, nesta pasta estão presentes as spiders com os códigos de extração.
- Na pasta **data_exploration_and_visualization**, estão presentes o código do dashboard shiny (na pasta app_imoveisolx) e o código de limpeza e transformação dos dados extraídos.
- Na pasta **sql**, estão presentes os códigos de criação das tabelas **imoveisolx** e **imoveisolx_transformed**.

