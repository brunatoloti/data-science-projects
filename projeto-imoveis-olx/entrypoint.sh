#! /bin/sh

airflow db init
airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
nohup airflow webserver -p 8080 &
nohup airflow scheduler 