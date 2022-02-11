from datetime import timedelta
from airflow.operators.bash_operator import BashOperator
from airflow import DAG
import pendulum


default_args = {
    'owner': 'bruna',
    'depends_on_past': False,
    'retries': 0,
    'start_date': pendulum.yesterday(tz='America/Sao_Paulo')
}


with DAG('crawler-imoveis-olx',
         default_args=default_args,
         description='DAG CRAWLER IMOVEIS OLX',
         schedule_interval=None
         ) as dag:
    ac = BashOperator(task_id='ac',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/ac.py')
    al = BashOperator(task_id='al',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/al.py')
    am = BashOperator(task_id='am',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/am.py')
    ap = BashOperator(task_id='ap',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/ap.py')
    ba = BashOperator(task_id='ba',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/ba.py')
    ce = BashOperator(task_id='ce',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/ce.py')
    df = BashOperator(task_id='df',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/df.py')
    es = BashOperator(task_id='es',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/es.py')
    go = BashOperator(task_id='go',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/go.py')
    ma = BashOperator(task_id='ma',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/ma.py')
    mg = BashOperator(task_id='mg',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/mg.py')
    ms = BashOperator(task_id='ms',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/ms.py')
    mt = BashOperator(task_id='mt',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/mt.py')
    pa = BashOperator(task_id='pa',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/pa.py')
    pb = BashOperator(task_id='pb',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/pb.py')
    pe = BashOperator(task_id='pe',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/pe.py')
    pi = BashOperator(task_id='pi',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/pi.py')
    pr = BashOperator(task_id='pr',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/pr.py')
    rj = BashOperator(task_id='rj',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/rj.py')
    rs = BashOperator(task_id='rs',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/rs.py')
    ro = BashOperator(task_id='ro',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/ro.py')
    rr = BashOperator(task_id='rr',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/rr.py')
    rn = BashOperator(task_id='rn',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/rn.py')
    sc = BashOperator(task_id='sc',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/sc.py')
    se = BashOperator(task_id='se',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/se.py')
    to = BashOperator(task_id='to',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/to.py')
    sp = BashOperator(task_id='sp',
                      bash_command='python3 /projeto-imoveis-olx/data_extraction/imoveisolx/spiders/sp.py')

    ac >> al >> am >> ap
    ba >> ce >> df >> es
    go >> ma >> mg >> ms
    mt >> pa >> pb >> pe
    pi >> rj >> rs >> ro
    rr >> sc >> se >> to
    sp >> pr >> rn

if __name__ == '__main__':
    dag.cli()