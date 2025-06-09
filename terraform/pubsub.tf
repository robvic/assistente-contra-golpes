resource "google_pubsub_topic" "eventarc-dev" {
  name = "eventarc-dev"
  labels = local.labels
}

resource "google_pubsub_subscription" "handler-dev" {
  name  = "handler-sub-dev"
  labels = local.labels
  topic = google_pubsub_topic.eventarc-dev.id

  message_retention_duration = "1200s"
  ack_deadline_seconds = 120

  retry_policy {
    minimum_backoff = "100s"
  }

  push_config {
    push_endpoint = "https://example.com/push"

    attributes = {
      x-goog-version = "v1"
    }
  }
}