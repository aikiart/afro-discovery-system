import json
import requests
import google.auth.transport.requests
import google.oauth2.service_account

KEY_PATH = r"I:\afro-discovery-system\serviceAccount.json"
PROJECT_ID = "afro-discovery-system"
COLLECTION = "afro_centric_apps"

# Target exact URL string
TARGET_URL = "https://helloblackworld.com/"

creds = google.oauth2.service_account.Credentials.from_service_account_file(
    KEY_PATH, 
    scopes=["https://www.googleapis.com/auth/datastore"]
)
req = google.auth.transport.requests.Request()
creds.refresh(req)

headers = {"Authorization": f"Bearer {creds.token}"}
base_endpoint = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{COLLECTION}"

# Fetch all documents across pages
all_documents = []
next_page_token = None

while True:
    params = {"pageSize": 300}
    if next_page_token:
        params["pageToken"] = next_page_token

    res = requests.get(base_endpoint, headers=headers, params=params)
    if res.status_code != 200:
        print(f"Error fetching docs: {res.status_code}")
        break

    data = res.json()
    all_documents.extend(data.get("documents", []))
    next_page_token = data.get("nextPageToken")
    if not next_page_token:
        break

print(f"Scanning {len(all_documents)} documents for exact URL match: '{TARGET_URL}'...")

deleted_count = 0
for doc in all_documents:
    fields = doc.get("fields", {})
    # Safely extract the exact 'url' string value from Firestore fields structure
    doc_url = fields.get("url", {}).get("stringValue", "").strip().rstrip('/')
    clean_target = TARGET_URL.strip().rstrip('/')

    if doc_url.lower() == clean_target.lower():
        doc_name = doc["name"]
        delete_url = f"https://firestore.googleapis.com/v1/{doc_name}"
        del_res = requests.delete(delete_url, headers=headers)
        
        if del_res.status_code == 200:
            doc_id = doc_name.split("/")[-1]
            print(f"🔥 Successfully deleted target document: {doc_id}")
            deleted_count += 1
        else:
            print(f"⚠️ Failed to delete {doc_name}: {del_res.status_code}")

if deleted_count == 0:
    print("ℹ️ No document found matching that exact URL.")
else:
    print(f"\nTargeted deletion complete. Total documents removed: {deleted_count}")