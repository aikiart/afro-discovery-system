import json
import requests
import google.auth.transport.requests
import google.oauth2.service_account

KEY_PATH = r"I:\afro-discovery-system\serviceAccount.json"
PROJECT_ID = "afro-discovery-system"
COLLECTION = "afro_centric_apps"

# Authenticate with Service Account
creds = google.oauth2.service_account.Credentials.from_service_account_file(
    KEY_PATH, 
    scopes=["https://www.googleapis.com/auth/datastore"]
)
req = google.auth.transport.requests.Request()
creds.refresh(req)

all_documents = []
next_page_token = None
base_endpoint = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{COLLECTION}"
headers = {"Authorization": f"Bearer {creds.token}"}

print("🔄 Starting paginated backup from Firestore...")

while True:
    params = {"pageSize": 300}
    if next_page_token:
        params["pageToken"] = next_page_token

    response = requests.get(base_endpoint, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ Error fetching documents: {response.status_code} {response.text}")
        break

    data = response.json()
    docs = data.get("documents", [])
    all_documents.extend(docs)

    print(f"   Fetched page: {len(docs)} documents (Total so far: {len(all_documents)})")

    next_page_token = data.get("nextPageToken")
    if not next_page_token:
        break

# Save all records locally
backup_filename = "firestore_backup.json"
with open(backup_filename, "w", encoding="utf-8") as f:
    json.dump(all_documents, f, indent=2)

print(f"\n✅ Success! Fully backed up ALL {len(all_documents)} documents to '{backup_filename}'.")