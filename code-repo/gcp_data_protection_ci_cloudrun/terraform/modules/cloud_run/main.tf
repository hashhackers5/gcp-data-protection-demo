
resource "google_cloud_run_v2_service" "default" {
  name     = var.function_name
  location = var.region
  template {
    containers {
      image = "gcr.io/infra-voyage-466111-u7/classifier-service"
      ports {
        container_port = 8080
      }
    }
    timeout = "3600s"  # Increase timeout to 1 hour
  }
}
