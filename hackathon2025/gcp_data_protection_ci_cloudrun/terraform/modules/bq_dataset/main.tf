
resource "google_bigquery_dataset" "default" {
  dataset_id = var.dataset_id
  location   = "US"
}
