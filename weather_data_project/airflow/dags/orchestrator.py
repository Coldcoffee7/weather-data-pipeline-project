from airflow.sdk import dag, task
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/api-request')

@dag(
    dag_id='weather_api_orchestrator',
    start_date=datetime(2026, 3, 24),
    schedule=timedelta(minutes=5),
    catchup=False
)
def weather_dag():

    @task
    def safe_main_callable():
        from insert_records import main
        main()

    safe_main_callable()

weather_dag()
