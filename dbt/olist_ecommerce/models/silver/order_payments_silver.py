import pyspark.sql.functions as F

def model(dbt,session):
    dbt.config(materialized='table')

    bucket_path = "gs://olist_ecomerce_bucket/raw_data/olist_order_payments_dataset.csv"

    bronze_df=session.read.format('csv').option('inferSchema','true').option('header','true').load(bucket_path)

    silver_df = bronze_df.filter(
        F.col('payment_value')>=0
        )

    return silver_df