import psycopg2
import pandas as pd


def get_data():
    con_pro = psycopg2.connect(host='postgres', database='airflow', user='airflow', password='airflow', port=5432)
    cur_pro = con_pro.cursor()
    cols = ['id', 'categoria', 'tipo', 'quartos', 'banheiros', 'vagas_garagem', 'detalhes_imovel', 'detalhes_condominio',
            'cep', 'cidade', 'estado', 'bairro', 'preco', 'url', 'operacao', 'created_at']
    sql = """
        SELECT * FROM imoveisolx_transformed;
    """
    cur_pro.execute(sql)
    recset = cur_pro.fetchall()
    db = pd.DataFrame(recset, columns=cols)
    con_pro.close()
    return db