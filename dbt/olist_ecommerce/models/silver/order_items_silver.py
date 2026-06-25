import pyspark.sql.functions as F

def model(dbt,session):

    dbt.config(materialized='table')
    
    bucket_path = 'gs://olist_ecomerce_bucket/raw_data/olist_order_items_dataset.csv'

    bronze_df = session.read.format('csv').option('inferSchema','true').option('header','true').option('timestampFormat','yyyy-MM-dd HH:mm:ss').load(bucket_path)

    silver_df = bronze_df.filter(
        (F.col('freight_value') >= 0) &
        (F.col('price') >= 0) &
        (F.col('shipping_limit_date').isNotNull())
    )

    return silver_df