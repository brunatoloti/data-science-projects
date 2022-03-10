import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime
from sqlalchemy import create_engine


def con_db():
    con = psycopg2.connect(host='postgres', 
                           database='airflow',
                           user='airflow',
                           password='airflow')
    return con

def get_db():
    con = con_db()
    cur = con.cursor()
    # cur.execute(f"SELECT * FROM imoveisolx WHERE created_at>='{datetime.now().strftime('%Y-%m-%d')}'")
    cur.execute(f"SELECT * FROM imoveisolx;")
    recset = cur.fetchall()

    db = pd.DataFrame(recset, columns=['id','categoria','tipo','quartos','banheiros','vagas_garagem','detalhes_imovel','detalhes_condominio','cep','cidade','estado','bairro','preco','url','created_at'])
    return db

def cleaning():
    df = get_db()
    df[['quartos', 'banheiros', 'vagas_garagem']] = df[['quartos', 'banheiros', 'vagas_garagem']].fillna('0') 
    df.quartos = df.quartos.str.replace(' ou mais', '')
    df.banheiros = df.banheiros.str.replace(' ou mais', '')
    df.vagas_garagem = df.vagas_garagem.str.replace(' ou mais', '')
    df.quartos = df.quartos.astype('int')
    df.banheiros = df.banheiros.astype('int')
    df.vagas_garagem = df.vagas_garagem.astype('int')
    df = df.dropna(subset=['preco'])
    df['preco'] = df['preco'].str.replace('.','').astype('float')
    df = df.drop(df.query("preco == 0.0").index)
    df = df.dropna(subset=['cidade'])
    df.tipo = df.tipo.fillna('Não informado')
    df.detalhes_imovel = df.detalhes_imovel.fillna('Não informado')
    df.detalhes_condominio = df.detalhes_condominio.fillna('Não informado')
    df.bairro = df.bairro.fillna('Não informado')
    df = df[~df.categoria.isin(['Aluguel - casas e apartamentos', 'Temporada'])]

    df_tipo_nao_informado = df[df.tipo.isin(['Não informado'])]
    df_tipo_informado = df[~df.tipo.isin(['Não informado'])]
    df_tipo_informado['operacao'] = df_tipo_informado.tipo.str.split('-').str[0]
    df_tipo_nao_informado['operacao'] = 'Não informado'

    novo_df = pd.concat([df_tipo_informado, df_tipo_nao_informado])
    novo_df = novo_df[['id','categoria','tipo','quartos','banheiros','vagas_garagem','detalhes_imovel','detalhes_condominio','cep','cidade','estado','bairro','preco','url','operacao','created_at']]
    return novo_df

def get_dados_limpos():
    con = con_db()
    cur = con.cursor()
    cur.execute(f"SELECT * FROM imoveisolx_transformed;")
    recset = cur.fetchall()

    df_antigo = pd.DataFrame(recset, columns=['id','categoria','tipo','quartos','banheiros','vagas_garagem','detalhes_imovel','detalhes_condominio','cep','cidade','estado','bairro','preco','url','operacao','created_at'])
    df_antigo.quartos = df_antigo.quartos.astype('int')
    df_antigo.banheiros = df_antigo.banheiros.astype('int')
    df_antigo.vagas_garagem = df_antigo.vagas_garagem.astype('int')
    return df_antigo

def save_db(df):
    engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres:5432/airflow')
    con = engine.connect()
    df.to_sql('imoveisolx_transformed', con=con, index=False)

def run():
    df = cleaning()
    df_antigo = get_dados_limpos()
    df = pd.concat([df_antigo, df])
    df = df.drop_duplicates(subset=['categoria','tipo','quartos','banheiros','vagas_garagem','detalhes_imovel','detalhes_condominio','cep','cidade','estado','bairro','preco','url','operacao'])
    save_db(df)

if __name__=='__main__':
    run()