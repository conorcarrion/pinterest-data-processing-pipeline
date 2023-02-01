from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from run import run


# Default arguments for the DAG
default_args = {
    "owner": "Conor Quinn",
    "start_date": datetime.now().date(),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    "run_dag",
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


batch_processor_task
