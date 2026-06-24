import pyspark.sql.functions as F

def model(dbt,session):

    dbt.config(materialized='table')
    bucket_path= 'gs://olist_ecomerce_bucket/raw_data/olist_geolocation_dataset.csv'
    mapping_path ='gs://olist_ecomerce_bucket/raw_data/raw_data_unique_geolocation_cities.csv'

    dict_df = session.read.format('csv').option('inferSchema','true').option('header','true').load(mapping_path)
    bronze_df = session.read.format('csv').option('inferSchema','true').option('header','true').load(bucket_path)

    chars_to_remove = "ãáàâäçéêèëíîìïóôõòöúûùüąćęłńśżź"
    chars_to_insert    = "aaaaaceeeeiiiiooooouuuuacelnśzz"

    cleaned_df = bronze_df.withColumn('geolocation_city',F.lower(F.regexp_replace(F.translate(F.col('geolocation_city'),chars_to_remove,chars_to_insert),"[^a-z]","")))
    dict_df = dict_df.filter(F.col('correct_name') != "CHECK_MANUALLY")


    cleaned_df = cleaned_df.join(
        F.broadcast(dict_df),
        cleaned_df.geolocation_city == dict_df.cleaned_name ,
        how='inner'
    )

    silver_df =cleaned_df.withColumn(
        'geolocation_city',
        F.col('correct_name').alias('geolocation_city')
    ).drop('cleaned_name','correct_name','occurrences')

    return silver_df