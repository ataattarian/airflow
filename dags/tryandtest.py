from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.docker_swarm_operator import DockerSwarmOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 25),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'docker_swarm_example',
    default_args=default_args,
    description='A DAG to deploy a Docker service on Swarm',
    schedule_interval=timedelta(days=1),
)

def check_docker_connection():
    import docker
    client = docker.from_env()
    try:
        version = client.version()
        print(f"Connected to Docker API version: {version}")
    except docker.errors.APIError as e:
        print(f"Error connecting to Docker API: {e}")

check_docker_task = PythonOperator(
    task_id='check_docker_connection',
    python_callable=check_docker_connection,
    dag=dag,
)

deploy_service_task = DockerSwarmOperator(
    task_id='deploy_service',
    image='192.168.12.50:5000/web:latest',
    api_version='auto',
    auto_remove=True,
    command='echo hello my name is ata',
    docker_url='tcp://192.168.12.50:2377',
    network_mode='bridge',
    dag=dag,
)

check_docker_task >> deploy_service_task

if __name__ == "__main__":
    dag.cli()
