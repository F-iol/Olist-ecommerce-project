from datetime import datetime
import pendulum
from airflow.sdk import dag,task
from assets import gold_data_ready,silver_data_ready
from cosmos import ProjectConfig, ProfileConfig, ExecutionConfig,DbtTaskGroup,RenderConfig
from cosmos.profiles import GoogleCloudOauthProfileMapping
import json


class HardcodedGcpOauthMapping(GoogleCloudOauthProfileMapping):
    @property
    def profile(self):
        CREDS_PATH = '/opt/airflow/.config/gcloud/application_default_credentials.json'
        with open(CREDS_PATH,'r') as f:
            adc = json.load(f)

        return { 
            "type":'bigquery',
            'method':'oauth',
            'project':'olist-ecomerce-project',
            'dataset':'olist_ecommerce_data_silver',
            'threads':4,
            'refresh_token':adc.get('refresh_token'),
            'client_id':adc.get('client_id'),
            'client_secret':adc.get('client_secret'),
            'location':'us-central1'
        }
    
render_config = RenderConfig(
    select=[
        'path:models/gold',
    ],
    test_behavior='after_all'
)

profile_config= ProfileConfig(
    profile_name='olist_ecommerce',
    target_name='dev',
    profile_mapping= HardcodedGcpOauthMapping(conn_id='gcp_dbt_conn')
)

project_config=ProjectConfig(
    dbt_project_path="/opt/airflow/dbt/olist_ecommerce",
    manifest_path="/opt/airflow/dbt/olist_ecommerce/target/manifest.json",
)

execution_config=ExecutionConfig(
    dbt_executable_path='/usr/local/bin/dbt'
)

@dag(
    dag_id='3_silver_to_gold',
    start_date=pendulum.datetime(2026,6,29,tz='Europe/Warsaw'),
    catchup=False,
    max_active_runs=1,
    max_active_tasks=1,
    schedule=[silver_data_ready],
    is_paused_upon_creation=False
)
def silver_to_gold():

    dbt_gold_layer = DbtTaskGroup(
        group_id ='dbt_gold_models',
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=render_config,
        default_args={
            'outlets':[gold_data_ready],
            'retries':10,
        }
    )
    dbt_gold_layer

silver_to_gold()