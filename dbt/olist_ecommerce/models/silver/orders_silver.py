import pyspark.sql.functions as F

def model(dbt,session):
    dbt.config(materialized ='table')

    bucket_path = "gs://olist_ecomerce_bucket/raw_data/olist_orders_dataset.csv"

    bronze_df = session.read.format('csv').option('header','true').option('inferSchema','true').load(bucket_path)

    silver_df = bronze_df.withColumn(
        F.col('order_status'), F.when(F.col('order_status')=='canceled','cancelled') \
        .otherwise(F.col('order_status'))
    )

    return silver_df