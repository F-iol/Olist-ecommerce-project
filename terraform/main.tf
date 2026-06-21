terraform {
  required_providers {
    google = {
        source = "hashicorp/google"
        version ="~>5.0"
    }
  }
}

provider "google" {
    project = "olist-ecomerce-project"
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
}

resource "google_bigquery_dataset" "bronze" {
    dataset_id = "olist_ecommerce_data_bronze"
    description = "Dataset for bronze"
    location = var.location
    delete_contents_on_destroy = true
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