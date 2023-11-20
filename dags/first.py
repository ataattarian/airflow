from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
import pendulum


def first_task():
    print('hello airflow')

with DAG(
    dag_id="example_python_operator",
    schedule=None,
    start_date=pendulum.datetime(2023, 11, 19, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    operator = PythonOperator(
        task_id='my_first_dag',
        python_callable=first_task,
        dag=dag,
    )
    
    t2 = DockerOperator(
        task_id='docker_command_sleep',
        image='python:3.8.0',
        container_name='task___command_sleep',
        api_version='auto',
        auto_remove=True,
        command="echo hello",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
        )
    