from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from run import run


# Default arguments for the DAG
default_args = {
    "owner": "me",
    "start_date": days_ago(2),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    "batch_processor_dag",
    default_args=default_args,
    schedule_interval="0 0 * * *",  # Run daily at midnight
    catchup=False,
)

# Create the task using the PythonOperator
batch_processor_task = PythonOperator(
    task_id="run_batch_processor",
    python_callable=run,
    dag=dag,
)

# Set the task dependencies
batch_processor_task
