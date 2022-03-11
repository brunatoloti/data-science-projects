import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras
from datetime import datetime
import hashlib


def con_db():
    con = psycopg2.connect(host='postgres', 
                           database='airflow',
                           user='airflow',
                           password='airflow')
    return con

def get_db():
    con = con_db()
    cur = con.cursor()
    cur.execute(f"SELECT * FROM imoveisolx WHERE created_at>='{datetime.now().strftime('%Y-%m-%d')}'")
    recset = cur.fetchall()

    db = pd.DataFrame(recset, columns=['id','categoria','tipo','quartos','banheiros','vagas_garagem','detalhes_imovel','detalhes_condominio','cep','cidade','estado','bairro','preco','url','created_at'])
    con.close()
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
    novo_df = novo_df.drop_duplicates(subset=['categoria','tipo','quartos','banheiros','vagas_garagem','detalhes_imovel','detalhes_condominio','cep','cidade','estado','bairro','preco','url','operacao'])
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
    con.close()
    return df_antigo

def save_db(df):
    values = []
    for row in df.itertuples():
        values.append({'id': row.id,
                       'categoria': row.categoria,
                       'tipo': row.tipo,
                       'quartos': row.quartos,
                       'banheiros': row.banheiros,
                       'vagas_garagem': row.vagas_garagem,
                       'detalhes_imovel': row.detalhes_imovel,
                       'detalhes_condominio': row.detalhes_condominio,
                       'cep': row.cep,
                       'cidade': row.cidade,
                       'estado': row.estado,
                       'bairro': row.bairro,
                       'preco': row.preco,
                       'url': row.url,
                       'operacao': row.operacao,
                       'created_at': row.created_at})
    print(f'-> # rows to be inserted: {len(values)}')
    values = iter(values)

    sql = """INSERT INTO imoveisolx_transformed(id,categoria,tipo,quartos,banheiros,vagas_garagem,detalhes_imovel,detalhes_condominio,cep,cidade,estado,bairro,preco,url,operacao,created_at)
             VALUES (%(id)s,%(categoria)s,%(tipo)s,%(quartos)s,%(banheiros)s,%(vagas_garagem)s,%(detalhes_imovel)s,%(detalhes_condominio)s,%(cep)s,%(cidade)s,%(estado)s,%(bairro)s,%(preco)s,%(url)s,%(operacao)s,%(created_at)s);"""
    con = con_db()
    cur = con.cursor()
    psycopg2.extras.execute_batch(cur, sql, values)
    con.commit()
    con.close()

def add_hash(df):
    df['hash'] =  df.categoria + df.tipo + df.quartos.astype(dtype=str) + df.banheiros.astype(dtype=str) + df.vagas_garagem.astype(dtype=str) + df.detalhes_imovel + df.detalhes_condominio + df.cep + df.cidade + df.estado + df.bairro + df.preco.astype(dtype=str) + df.url + df.operacao
    df['hash'] = df['hash'].apply(lambda x: hashlib.shake_128(x.encode('utf-8')).hexdigest(8))
    return df

def merge_dataframes(df, df_antigo):
    merge_df = pd.merge(df_antigo, df, 
                        left_on=['hash'], right_on=['hash'],
                        how='outer',
                        suffixes=('_db', ''))
    merge_df = merge_df[merge_df['id_db'].isna()]
    return merge_df

def run():
    df = cleaning()
    df_antigo = get_dados_limpos()
    df = add_hash(df)
    df_antigo = add_hash(df_antigo)
    df = merge_dataframes(df, df_antigo)
    save_db(df)

if __name__=='__main__':
    run()