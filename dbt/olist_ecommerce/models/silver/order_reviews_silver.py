import pyspark.sql.functions as F

def model(dbt,session):
    dbt.config(materialized='table')

    bucket_path = "gs://olist_ecomerce_bucket/raw_data/olist_order_reviews_dataset.csv"

    bronze_df = session.read.format('csv').option('header','true').option('inferSchema','true').load(bucket_path)

    silver_df = bronze_df.filter(
        (F.col('review_score').between(1,5)) &
        (F.col('review_creation_date').isNotNull()) &
        (F.col('review_answer_timestamp').isNotNull())
    )

    return silver_df