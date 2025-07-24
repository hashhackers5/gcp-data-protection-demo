resource "google_data_loss_prevention_inspect_template" "default" {
  parent       = "projects/${var.project_id}"
  template_id = "example-inspect-template"
  display_name = "Example Inspect Template"

  inspect_config {
    info_types {
      name = "PHONE_NUMBER"
    }
    info_types {
      name = "EMAIL_ADDRESS"
    }

    min_likelihood = "POSSIBLE"
    limits {
      max_findings_per_request = 100
	  max_findings_per_item    = 100
    }
    include_quote = true
  }

  description = "Template for inspecting phone numbers and emails"
}