from airflow.decorators import dag,task
from assets import silver_data_ready
from datetime import datetime
import pendulum
from ingestion.ingestion import download_kaggle_to_gcs

@dag(
    dag_id = '1_fetch_to_raw_data',
    start_date=pendulum.datetime(2026,6,29,tz='Europe/Warsaw'),
    max_active_runs=1,
    schedule=None,
    catchup=False,
)
def fetch_to_bucket():
    
    @task(outlets=[silver_data_ready])
    def fetch_data():
        try:
            download_kaggle_to_gcs(
                'olistbr/brazilian-ecommerce',
                'olist_ecomerce_bucket',
                'olist-ecomerce-project')
            
            print('ingestion successfuly finished')
        except Exception as e:
            print(f'Error with ingestion file: {e}')
            raise e

    fetch_data()

fetch_to_bucket()