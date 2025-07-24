
resource "google_data_catalog_taxonomy" "taxonomy" {
  display_name = "PII Classification"
  region       = var.region
  activated_policy_types = ["FINE_GRAINED_ACCESS_CONTROL"]
}

resource "google_data_catalog_policy_tag" "email" {
  taxonomy     = google_data_catalog_taxonomy.taxonomy.id
  display_name = "EMAIL_ADDRESS"
}
