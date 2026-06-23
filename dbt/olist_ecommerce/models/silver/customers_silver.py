from pyspark.sql.functions import col,initcap,trim,current_timestamp,upper

def model(dbt,session):
    dbt.config(materialized='table')

    bucket_path = "gs://olist_ecomerce_bucket/raw_data/olist_customers_dataset.csv" # I DONT KNOW WHY I CANT PULL THIS FROM DBT_PROJECT.YML BUT IT DRIVES ME INSNAE

    bronze_df = session.read.format('csv').option('header','true').option('inferSchema','true').load(bucket_path)

    silver_df = bronze_df.select(
        col('customer_id'),
        col('customer_unique_id'),
        col('customer_zip_code_prefix'),
        initcap(trim(col('customer_city'))).alias('customer_city'),
        upper(col('customer_state')).alias('customer_state'),
        current_timestamp().alias("ingested_at")
    )


    return silver_df