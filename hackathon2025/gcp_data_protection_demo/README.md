
# GCP Data Protection Framework (Live Demo)

End-to-end solution demonstrating:
1. Raw Data Ingestion
2. Sensitive Data Scanning (Cloud DLP)
3. Metadata Tagging (Data Catalog/Dataplex)
4. Automated Classification Engine
5. Policy Enforcement via BigQuery Views/UDFs
6. IAM/VPC-SC Secure Access Control
7. Audit & Monitoring

## 🚀 Quick Start

- Modify `terraform/variables.tf` with your GCP settings
- Deploy Terraform: `cd terraform && terraform init && terraform apply`
- Upload raw data to BigQuery (see `bq_ingestion/load_sample.py`)
- Watch automated DLP scan + tagging + masking trigger via Cloud Function
- Use BigQuery views/UDFs to securely query data
