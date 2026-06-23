# Overview

End-to-end data engineering project on Google Cloud Platform implementing a scalable ELT pipeline. The system uses Airflow for orchestration, Terraform for infrastructure provisioning, PySpark for data processing, and dbt for analytics modeling. Data is ingested from Kaggle datasets into a cloud-based data lake architecture.


# Mermaid diagram
for now more or less it looks like this:

```mermaid
flowchart LR

A[Terraform] --> B["GCP Setup<br/>Service Accounts + Infrastructure<br/>Silver Datasets"]

C[Kaggle Dataset] --> D["ingestion.py"]
D --> E["Google Cloud Storage Bucket<br/>Bronze / Raw Data"]

E --> F["PySpark Jobs"]
F --> G["Silver Tables - Cleaned & Structured"]

G --> H["To be continued"]
```

# Current problems and approaches

### Pyspark / dbt
Why Pyspark in such simple transformations in silver layer ? - I really wanted try out pyspark with dbt so i decided on a whim using Pyspark here even tho it's pretty much unnecessary <br>
At first idea was to use External Tables in gcp bigquery for bronze layer but I really struggled to debug some problems with storage api , Pyspark kept on throwing errors probably wouldnt be a case if I used SQL instead. <br>
Tried different approach to use buckets for keeping raw data=bronze layer so now I read data directly from the bucket and removed bronze_dataset as it's unnecessary now<br>
Another problem with Pyspark in gcp - for whatever reason whenever I submit a batch query for Pyspark it doesn't send my dbt_project.yml along so I cannot use variables declared inside and have to hardcode them inside each .py file <br>
Problems with service accounts I actually don't know why it happend but despite having declared Service account for spark it kept on using default one - kinda resolved with terraform as I don't create seperate new iam member but just add permissions directly from terraform.tf file to default service account so no need to give permissions 'on fly' with CLI<br>