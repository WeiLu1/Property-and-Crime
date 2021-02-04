from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from main import insert_crimes_to_db


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['weiman96@hotmail.co.uk'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),

}

dag = DAG(
    'police_postgres',
    default_args=default_args,
    schedule_interval='0 9 * * 1',
    start_date=days_ago(2)
)


t1 = PythonOperator(
    task_id='insert',
    python_callable=insert_crimes_to_db,
    dag=dag
)


t1