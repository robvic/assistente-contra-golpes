terraform {
  backend "http" {
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