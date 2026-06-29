from datetime import datetime
import pendulum
from airflow.sdk import dag,task
from assets import bronze_data_ready,silver_data_ready
from cosmos import ProjectConfig, ProfileConfig, ExecutionConfig,DbtTaskGroup,RenderConfig
from cosmos.profiles import GoogleCloudOauthProfileMapping
import json
from google.cloud import storage


class HardcodedGcpOauthMapping(GoogleCloudOauthProfileMapping):
    @property
    def profile(self) -> dict:
        CREDENTIALS_PATH = '/opt/airflow/.config/gcloud/application_default_credentials.json'
        with open(CREDENTIALS_PATH, 'r') as f:
            adc = json.load(f)
            
        return {
            "type": "bigquery",
            "method": "oauth", 
            "project": "olist-ecomerce-project",
            "dataset": "olist_ecommerce_data_silver",
            "threads": 1,
            "refresh_token": adc.get("refresh_token"),
            "client_id": adc.get("client_id"),
            "client_secret": adc.get("client_secret"),
            "dataproc_region":'us-central1',
            "location":'us-central1',
            "gcs_bucket":"olist_ecomerce_bucket",
            "dataproc_properties": {
                "dataproc:dataproc.master.machine.type": "n1-standard-2",
                "dataproc:dataproc.worker.machine.type": "n1-standard-2",
                "dataproc:dataproc.master.disk.size.gb": "30",
                "dataproc:dataproc.worker.disk.size.gb": "30"
            }
        }
    
render_config = RenderConfig(
    select=['path:seeds/raw_data_unique_geolocation_cities.csv',
            'path:models/silver'
            ],
            test_behavior='after_all'
)

profile_config=ProfileConfig( 
    profile_name = 'olist_ecommerce',
    target_name='dev',
    profile_mapping = HardcodedGcpOauthMapping(conn_id='gcp_dbt_conn')
)


@dag(
    dag_id = '2_bronze_to_silver',
    start_date=pendulum.datetime(2026,6,29,tz='Europe/Warsaw'),
    max_active_runs = 1,
    max_active_tasks=1,
    catchup=False,
    schedule=[bronze_data_ready],
    is_paused_upon_creation=False
)
def bronze_to_silver():


    @task.python
    def upload_to_bucket():
        client = storage.Client(project='olist-ecomerce-project')
        bucket = client.bucket('olist_ecomerce_bucket')
        blob = bucket.blob('raw_data/raw_data_unique_geolocation_cities.csv')
        blob.upload_from_filename('/opt/airflow/include/raw_data_unique_geolocation_cities.csv')
        print("Geo cities sent to bucket")


    dbt_silver_layer=DbtTaskGroup(
        group_id = 'dbt_silver_models',
        project_config =ProjectConfig(
            dbt_project_path ="/opt/airflow/dbt/olist_ecommerce",
            manifest_path="/opt/airflow/dbt/olist_ecommerce/target/manifest.json",
            ),
        profile_config=profile_config,
        execution_config=ExecutionConfig(dbt_executable_path="/usr/local/bin/dbt"),
        render_config=render_config,
        default_args={'outlets':[silver_data_ready],'retries':10}
    )
    upload_to_bucket()>>dbt_silver_layer

bronze_to_silver()