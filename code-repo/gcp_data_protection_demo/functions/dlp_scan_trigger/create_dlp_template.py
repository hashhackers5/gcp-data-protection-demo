from google.cloud import dlp_v2

# Initialize client
client = dlp_v2.DlpServiceClient()
parent = "projects/infra-voyage-466111-u7/locations/global"

# Define the inspect config (what types of sensitive data to scan for)
inspect_config = {
    "info_types": [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
    ],
    "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
    "include_quote": True,
}

# Define template metadata
template = {
    "inspect_config": inspect_config,
    "display_name": "basic-inspect-template",
    "description": "Detects email, phone numbers, and credit card numbers",
}

# Create the template
response = client.create_inspect_template(
    request={"parent": parent, "inspect_template": template}
)

print(f" Created DLP inspect template: {response.name}")