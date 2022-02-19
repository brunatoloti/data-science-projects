import psycopg2


class Pipeline(object):
    def open_spider(self, spider):
        hostname = 'postgres'
        username = 'airflow'
        password = 'airflow'
        database = 'airflow'
        port = '5432'

        self.connection = psycopg2.connect(
            host = hostname,
            user = username,
            password = password,
            dbname = database,
            port = port
        )
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("""INSERT INTO imoveisolx(categoria,tipo,quartos,banheiros,vagas_garagem,detalhes_imovel,detalhes_condominio,cep,cidade,estado,bairro,preco,url) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (item['categoria'],item['tipo'],item['quartos'],item['banheiros'],item['vagas_garagem'],item['detalhes_imovel'],
                                                    item['detalhes_condominio'],item['cep'],item['cidade'],item['estado'],item['bairro'],item['preco'],item['url']))
        self.connection.commit()
        return item