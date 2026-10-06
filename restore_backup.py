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

# Read local JSON backup
with open("firestore_backup.json", "r", encoding="utf-8") as f:
    backup_docs = json.load(f)

print(f"📦 Loaded {len(backup_docs)} documents from 'firestore_backup.json'. Restoring...")

headers = {
    "Authorization": f"Bearer {creds.token}",
    "Content-Type": "application/json"
}

restored_count = 0
for doc in backup_docs:
    doc_name = doc["name"] # e.g. projects/.../documents/afro_centric_apps/doc_id
    endpoint = f"https://firestore.googleapis.com/v1/{doc_name}"
    
    payload = {"fields": doc.get("fields", {})}
    res = requests.patch(endpoint, headers=headers, json=payload)
    
    if res.status_code in (200, 201):
        restored_count += 1
        doc_id = doc_name.split("/")[-1]
        print(f"  ✅ Restored: {doc_id}")
    else:
        print(f"  ⚠️ Error restoring {doc_name}: {res.status_code} {res.text}")

print(f"\n🎉 Restoration complete! {restored_count} documents successfully restored to Firestore.")