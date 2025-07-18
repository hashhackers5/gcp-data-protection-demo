from flask import Flask, request, jsonify
from google.cloud import pubsub_v1, bigquery
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "infra-voyage-466111-u7")
PUBSUB_TOPIC = "classified-text-topic"
BQ_METADATA_DATASET = "metadata_repo"
BQ_METADATA_TABLE = "classification_metadata"

# Clients
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)
bq_client = bigquery.Client()

@app.route("/", methods=["POST"])
def classify():
    data = request.get_json()
    table_id = data.get("table_id")
    dataset_id = data.get("dataset_id", "your_dataset")
    text = data.get("text", "")

    # Dummy classification logic
    policy_tags = {
        "email": "EMAIL_ADDRESS",
        "phone": "PHONE_NUMBER",
        "credit_card": "CREDIT_CARD_NUMBER"
    }

    # Prepare message for Pub/Sub
    pubsub_payload = {
        "project_id": PROJECT_ID,
        "dataset_id": dataset_id,
        "table_id": table_id,
        "text": text
    }

    try:
        # Publish to Pub/Sub
        future = publisher.publish(topic_path, json.dumps(pubsub_payload).encode("utf-8"))
        future.result()

        # Write to Metadata Repository in BigQuery
        metadata_row = {
            "timestamp": datetime.utcnow().isoformat(),
            "project_id": PROJECT_ID,
            "dataset_id": dataset_id,
            "table_id": table_id,
            "tags": json.dumps(policy_tags),
            "source": "classifier"
        }

        table_ref = f"{PROJECT_ID}.{BQ_METADATA_DATASET}.{BQ_METADATA_TABLE}"
        bq_client.insert_rows_json(table_ref, [metadata_row])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "classified": True,
        "tags": policy_tags,
        "message": "Published to Pub/Sub and metadata recorded"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)