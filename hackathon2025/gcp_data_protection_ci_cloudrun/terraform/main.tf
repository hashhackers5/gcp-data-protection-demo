
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "bq_dataset" {
  source     = "./modules/bq_dataset"
  dataset_id = "demo_data"
}

module "dlp_findings" {
  source     = "./modules/bq_dataset"
  dataset_id = "dlp_results"
}

module "dlp_template" {
  source = "./modules/dlp_template"
  project_id = var.project_id
}

module "data_catalog" {
  source = "./modules/datacatalog"
  region     = var.region
}

module "cloud_run_classifier" {
  source = "./modules/cloud_run"
  project_id = var.project_id
  region     = var.region
  function_name = "classifier-service"
}
