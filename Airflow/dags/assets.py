from airflow.sdk import Asset


bronze_data_ready =Asset(
    name='gcs_olist_bronze_ready',
    uri = 'gs://olist_ecomerce_bucket/raw_data/'
)

silver_data_ready =Asset(
    name = 'bg_olist_silver_dataset',
    uri='bigquery://olist-ecomerce-project/olist_ecommerce_data_silver/orders'
)

gold_data_ready =Asset(
    name = 'bg_olist_gold_dataset',
    uri='bigquery://olist-ecomerce-project/olist_ecommerce_data_gold/orders'
)



