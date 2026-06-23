terraform {
  required_providers {
    google = {
        source = "hashicorp/google"
        version ="~>5.0"
    }
  }
}

provider "google" {
    project = var.project_id
    region =var.location
  
}

resource "google_storage_bucket" "olist_ecommerce" {
  name="olist_ecomerce_bucket"
  location = var.location
  storage_class = "STANDARD"
  force_destroy = true
  uniform_bucket_level_access = true

    lifecycle_rule {
    condition {
      age=1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
      lifecycle_rule {
    condition {
      age=1
    }
    action {
      type = "Delete"
    }
  }
}


resource "google_bigquery_dataset" "silver" {
    dataset_id = "olist_ecommerce_data_silver"
    description = "Dataset for silver"
    location = var.location
    delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "gold" {
    dataset_id = "olist_ecommerce_data_gold"
    description = "Dataset for gold"
    location = var.location
    delete_contents_on_destroy = true
}

data "google_project" "project" {
  project_id = var.project_id
}


resource "google_project_iam_member" "dbt_spark_bq" {
  project = var.project_id
  role = "roles/bigquery.admin"
  member = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

resource "google_project_iam_member" "dbt_spark_dataproc" {
  project = var.project_id
  role = "roles/dataproc.worker"
  member = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}