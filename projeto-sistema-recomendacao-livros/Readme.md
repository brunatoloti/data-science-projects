# Projeto de sistema de recomendação de livros (EM ANDAMENTO)

A ideia é criar um sistema de recomendação de livros usando python, streamlit, postgresql e docker.

Basicamente, será criada uma aplicação com streamlit onde o usuário será capaz de dar suas notas para o máximo possível de livros que ele quiser. Com isso computado, será retornado alguma/algumas recomendações de próximas leituras.
A ideia também é gravar essas notas que o usuário deu para alguns livros e armazená-las no banco de dados (postgresql). Dessa forma, conseguiremos aumentar ainda mais a base de dados e usar esses novos dados como alimento no sistema de recomendação.

As bases de dados foram obtidas no Kaggle e referem-se a dados da plataforma Goodreads.
Temos as seguintes tabelas:
- books
- books_tags
- ratings
- tags