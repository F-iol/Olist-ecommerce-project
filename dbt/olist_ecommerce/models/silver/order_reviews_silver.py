import pyspark.sql.functions as F

def model(dbt,session):
    dbt.config(materialized='table')

    bucket_path = "gs://olist_ecomerce_bucket/raw_data/olist_order_reviews_dataset.csv"

    __schema = 'review_id string,order_id string,review_score int, review_comment_title string,review_comment_message string,review_creation_date timestamp,review_answer_timestamp timestamp'
    bronze_df = session.read.format('csv').schema(__schema).option('header','true').option('multiLine','true').load(bucket_path)

    silver_df = bronze_df.filter(
        (F.col('review_score').between(1,5)) &
        (F.col('review_creation_date').isNotNull())
    )

    return silver_df