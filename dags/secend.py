from datetime import datetime,timedelta
from airflow import DAG
from airflow.contrib.operators.docker_swarm_operator import DockerSwarmOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 23),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate a DAG with the default_args
dag = DAG(
    'docker_swarm_example',
    default_args=default_args,
    description='A comprehensive example DAG to deploy a Docker service on Swarm',
    schedule_interval=timedelta(days=1),  # You can adjust the scheduling interval
)

# Define the task using DockerSwarmOperator
deploy_service_task = DockerSwarmOperator(
    task_id='deploy_service',
    image='192.168.12.50:5000/web:latest',  # Replace with your actual Docker image
    api_version='auto',  # You can specify the Docker API version if needed
    auto_remove=True,  # Remove the container once the task is finished
    command='echo hello',  # Replace with your actual Docker command
    dag=dag,
    network_mode='bridge'
)

# Set the task dependencies (if any)
# Example: deploy_service_task >> another_task

# You can continue to define more tasks and their dependencies as needed.

if __name__ == "__main__":
    dag.cli()
