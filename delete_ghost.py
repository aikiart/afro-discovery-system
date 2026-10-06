import json
import requests
import google.auth.transport.requests
import google.oauth2.service_account

KEY_PATH = r"I:\afro-discovery-system\serviceAccount.json"
PROJECT_ID = "afro-discovery-system"
COLLECTION = "afro_centric_apps"

creds = google.oauth2.service_account.Credentials.from_service_account_file(
    KEY_PATH, 
    scopes=["https://www.googleapis.com/auth/datastore"]
)
req = google.auth.transport.requests.Request()
creds.refresh(req)

endpoint = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{COLLECTION}"
headers = {"Authorization": f"Bearer {creds.token}"}

response = requests.get(endpoint, headers=headers)
if response.status_code != 200:
    print(f"Failed to fetch documents: {response.status_code} {response.text}")
    exit()

documents = response.json().get("documents", [])
print(f"Found {len(documents)} total documents in '{COLLECTION}'. Scanning for 'Hello Black World'...")

deleted_count = 0
for doc in documents:
    doc_dump = json.dumps(doc).lower()
    if "hello" in doc_dump or "blackworld" in doc_dump:
        doc_name = doc["name"]
        delete_url = f"https://firestore.googleapis.com/v1/{doc_name}"
        del_res = requests.delete(delete_url, headers=headers)
        if del_res.status_code == 200:
            doc_id = doc_name.split("/")[-1]
            print(f"🔥 Successfully deleted document: {doc_id}")
            deleted_count += 1
        else:
            print(f"Failed to delete {doc_name}: {del_res.status_code}")

print(f"\nCleanup complete. Total documents removed: {deleted_count}")