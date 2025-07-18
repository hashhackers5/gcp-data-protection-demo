# GCP Data Protection Project - Automated DLP Scanning & Access Management

## 🚀 Overview

This project implements a **serverless, automated data protection pipeline** on Google Cloud Platform (GCP) using Cloud DLP, BigQuery, Pub/Sub, Cloud Functions, and Cloud Scheduler.

It allows organizations to:

- Automatically scan BigQuery tables for sensitive data (PII/PHI)
- Apply de-identification (masking) transformations
- Store safe-to-use masked datasets
- Maintain metadata logs for audits
- Enforce fine-grained access control on sensitive data

---

## 📊 Architecture Components

### 1. **BigQuery**

- `metadata_repo.test_table` - Source table containing raw data
- `metadata_repo.masked_table` - Target table storing masked data
- `metadata_repo.classification_logs` - Logs of DLP job executions

### 2. **Cloud DLP**

- Inspects BigQuery tables for sensitive fields
- Applies masking using `ReplaceWithInfoTypeConfig`
- Stores results in masked tables and logs

### 3. **Cloud Scheduler**

- Triggers scans at regular intervals (e.g., daily)

### 4. **Pub/Sub**

- Topic: `classified-text-topic`
- Used as the event bus to trigger DLP scans

### 5. **Cloud Function**

- Name: `dlp_trigger`
- Trigger: Pub/Sub
- Executes DLP scan and updates metadata logs

---

## 🎓 Key Features

### ✅ Automated PII Discovery

Scans BigQuery datasets for:

- Email addresses
- Phone numbers
- Person names

### ✅ Data Masking

- Replaces sensitive data with infoType tokens (e.g., `[EMAIL_ADDRESS]`)
- Output stored in `masked_table`

### ✅ Secure Access Control

- Analysts: Can only access masked data (via views)
- Security team: Can access raw data via Cloud Run with IAM

### ✅ Metadata Logging

Each DLP job writes to `classification_logs` with:

- Project ID
- Dataset ID
- Table ID
- DLP job ID
- Timestamp
- Tags

---

## ⚙️ Deployment Instructions

### 1. Deploy Cloud Function

```powershell
gcloud functions deploy dlp_trigger `
  --entry-point=dlp_trigger `
  --runtime=python310 `
  --trigger-topic=classified-text-topic `
  --region=us-central1 `
  --set-env-vars=GOOGLE_CLOUD_PROJECT=infra-voyage-466111-u7
```

### 2. Grant Scheduler Publish Permission

```powershell
gcloud pubsub topics add-iam-policy-binding classified-text-topic `
  --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-cloudscheduler.iam.gserviceaccount.com" `
  --role="roles/pubsub.publisher" `
  --project=infra-voyage-466111-u7
```

### 3. Create Scheduler Job

```powershell
echo '{"project_id":"infra-voyage-466111-u7","dataset_id":"metadata_repo","table_id":"test_table","text":"Scheduled DLP Scan","tags":["pii","scheduled"]}' > dlp_payload.json

gcloud scheduler jobs create pubsub scheduled-dlp-job `
  --schedule="0 * * * *" `
  --time-zone="Asia/Kolkata" `
  --topic=classified-text-topic `
  --message-body-from-file=dlp_payload.json `
  --project=infra-voyage-466111-u7
```

---

## 📊 Sample Logs (from Cloud Function)

```
Parsed payload: {...}
DLP job started: projects/infra-voyage.../dlpJobs/i-2893...
BigQuery table updated successfully.
```

---

## 🚫 Access Control Model

| Role             | Access Level                   |
| ---------------- | ------------------------------ |
| General Analysts | Masked Data via BigQuery Views |
| Security Team    | Raw Data via Cloud Run + IAM   |

---

## 🎉 Outcomes

- Scalable, low-maintenance PII scanning
- Audit-ready metadata tracking
- Privacy-safe data for analytics & ML
- Aligned with privacy regulations (GDPR, HIPAA, etc.)

---

## 🚩 Future Improvements

- Add custom InfoTypes (e.g., Aadhaar, PAN)
- Integrate with Looker for dashboarding
- Auto-label columns in BigQuery with sensitivity tags
- Alerting via Cloud Monitoring

---

## 📄 Authors

- Ashirbad Ray (Hackathon 2025)

---

