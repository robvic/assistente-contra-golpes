resource "google_storage_bucket" "base-golpes-dev" {
  name = "base-golpes-dev"
  uniform_bucket_level_access = true
  labels = local.labels
  location = var.region
}

resource "google_storage_bucket" "base-golpes-sumarizado-dev" {
  name = "base-golpes-sumarizado-dev"
  uniform_bucket_level_access = true
  labels = local.labels
  location = var.region
}

resource "google_storage_bucket" "temp-handler-code" {
  name = "temp-handler-code"
  uniform_bucket_level_access = true
  labels = local.labels
  location = var.region
}

resource "google_storage_bucket" "bucket-instructions" {
  name = "bucket-instructions"
  uniform_bucket_level_access = true
  labels = local.labels
  location = var.region  
}

resource "google_storage_bucket_object" "object-instructions" {
  name = "ingest-instructions.txt"
  bucket = google_storage_bucket.bucket-instructions.name
  source = "../data/instructions/ingest-instruction.txt"
}
