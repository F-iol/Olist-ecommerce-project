import pyspark.sql.functions as F

def model(dbt,session):
    dbt.config(materialized='table')

    bucket_path = "gs://olist_ecomerce_bucket/raw_data/olist_sellers_dataset.csv"
    mapping_path ='gs://olist_ecomerce_bucket/raw_data/raw_data_unique_geolocation_cities.csv'

    dict_df = session.read.format('csv').option('inferSchema','true').option('header','true').load(mapping_path)
    bronze_df = session.read.format('csv').option('inferSchema','true').option('header','true').load(bucket_path)

    chars_to_remove = "ãáàâäçéêèëíîìïóôõòöúûùüąćęłńśżź"
    chars_to_insert    = "aaaaaceeeeiiiiooooouuuuacelnszz"

    silver_df = bronze_df.withColumn(
        'seller_city',F.lower(F.translate(F.col('seller_city'),chars_to_remove,chars_to_insert))
        )
    
    silver_df = silver_df.withColumns(
        {
        'seller_city': F.trim(F.regexp_replace(F.col('seller_city'),'[0-9,/\\-]','')),
        'seller_state': F.upper(F.col('seller_state'))
        }
    )
    
    silver_df = silver_df.filter(
        F.col('seller_id').isNotNull() 
    )

    matched_df =silver_df.join(
        F.broadcast(dict_df),
        F.trim(F.col('seller_city')).contains(F.trim(F.lower(F.col('correct_name')))),
        how='left_semi'
    )

    matched_df =matched_df.withColumn(
        'seller_city',F.initcap(F.expr("regexp_replace(seller_city,concat(' ?',lower(seller_state),'$'),'')"))
    )

    return matched_df