import base64
import json
from google.cloud import dlp_v2
from google.cloud import bigquery
from datetime import datetime

def dlp_trigger(event, context):
    # Handle missing or invalid 'data' in the event
    if 'data' not in event:
        print("Error: No 'data' field in event.")
        return

    try:
        decoded_data = base64.b64decode(event['data']).decode('utf-8')
    except Exception as e:
        print(f"Error decoding base64 data: {e}")
        return

    if not decoded_data.strip():
        print("Error: Decoded data is empty.")
        return

    try:
        payload = json.loads(decoded_data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from decoded data: {e}")
        return

    print("Parsed payload:", payload)

    project_id = payload.get('project_id')
    dataset_id = payload.get('dataset_id')
    table_id = payload.get('table_id')
    tags = payload.get('tags', [])
    text = payload.get('text', "")

    if not all([project_id, dataset_id, table_id]):
        print("Error: Missing required fields in payload (project_id, dataset_id, or table_id).")
        return

    dlp = dlp_v2.DlpServiceClient()
    bq_client = bigquery.Client()

    parent = f"projects/{project_id}/locations/global"
    table_ref = {
        "project_id": project_id,
        "dataset_id": dataset_id,
        "table_id": table_id
    }

    inspect_job = {
        "inspect_template_name": "projects/infra-voyage-466111-u7/locations/global/inspectTemplates/7200209525981729094",
        "storage_config": {
            "big_query_options": {
                "table_reference": table_ref
            }
        },
        "actions": [{
            "save_findings": {
                "output_config": {
                    "table": {
                        "project_id": project_id,
                        "dataset_id": "dlp_results",
                        "table_id": "dlp_findings"
                    }
                }
            }
        }]
    }

    try:
        response = dlp.create_dlp_job(parent=parent, inspect_job=inspect_job)
        dlp_job_name = response.name
        print("DLP job started:", dlp_job_name)
    except Exception as e:
        print(f"Error creating DLP job: {e}")
        return

    # Update metadata table with DLP job name
    try:
        table = f"{project_id}.metadata_repo.classification_logs"
        query = f"""
            UPDATE `{table}`
            SET dlp_job_name = @dlp_job_name
            WHERE project_id = @project_id
              AND dataset_id = @dataset_id
              AND table_id = @table_id
              AND text = @text
              AND dlp_job_name IS NULL
        """  # Removed LIMIT 1
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("dlp_job_name", "STRING", dlp_job_name),
                bigquery.ScalarQueryParameter("project_id", "STRING", project_id),
                bigquery.ScalarQueryParameter("dataset_id", "STRING", dataset_id),
                bigquery.ScalarQueryParameter("table_id", "STRING", table_id),
                bigquery.ScalarQueryParameter("text", "STRING", text),
            ]
        )
        query_job = bq_client.query(query, job_config=job_config)
        query_job.result()
        print("BigQuery table updated successfully.")
    except Exception as e:
        print("BigQuery update error:", e)