terraform {
  backend "gcs" {
    bucket = "terraform-icg-state"
    prefix = "env/dev"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.38.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}