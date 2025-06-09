resource "google_eventarc_trigger" "trigger-bucket-dev" {
  name     = "trigger-bucket-dev"
  location = var.region
  labels   = local.labels
  matching_criteria {
    attribute = "type"
    value     = "google.cloud.storage.object.v1.finalized"
  }
  matching_criteria {
    attribute = "bucket"
    value     = "base-golpes-dev"
  }
  destination {
    cloud_run_service {
      service = google_cloudfunctions_function.handler.name
      region  = var.region
    }
  }
  transport {
    pubsub {
      topic = google_pubsub_topic.eventarc-dev.id
    }
  }
}