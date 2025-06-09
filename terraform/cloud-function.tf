data "archive_file" "uploader-zip" {
  type = "zip"
  source_dir = "../src/cloud-function"
  output_path = "cf-export/uploader"
}

resource "google_storage_bucket_object" "uploader-code" {
  name = "${data.archive_file.uploader-zip.output_path}-${data.archive_file.uploader-zip.output_sha}.zip"
  bucket = google_storage_bucket.temp-handler-code.name
  source = data.archive_file.uploader-zip.output_path
}

# TESTE COM RESOURCE DE CF ANTIGO, NÃO ATIVAR!

# resource "google_cloudfunctions_function" "handler" {
#   name = "handler"
#   runtime = "python313"
#   event_trigger {
#     event_type = "google.pubsub.topic.publish"
#     resource = google_pubsub_topic.eventarc-dev.id
#   }
#   entry_point = "process"
#   labels = local.labels
  
#   source_archive_bucket = google_storage_bucket.temp-handler-code.name
#   source_archive_object = google_storage_bucket_object.uploader-code.name
# }

resource "google_cloud_run_v2_service" "handler" {
  name     = "handler"
  location = var.region

  template {
    containers {
      image = "ubuntu/python:3.13"
      command = ["/bin/bash", "-c"]
      args = [
        <<-EOT
            curl -o ${google_storage_bucket_object.uploader-code.name}
            https://storage.googleapis.com/${google_storage_bucket.temp-handler-code.name}/${google_storage_bucket_object.uploader-code.name} &&
            unzip ${google_storage_bucket_object.uploader-code.name} -d code &&
            python3 code/uploader.py
        EOT
      ]
      env {
        name = "PYTHONBUFFERED"
        value = "1"
      }
    }
  }
  
}