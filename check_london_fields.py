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

headers = {"Authorization": f"Bearer {creds.token}"}
base_endpoint = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{COLLECTION}"

all_documents = []
next_page_token = None

while True:
    params = {"pageSize": 300}
    if next_page_token:
        params["pageToken"] = next_page_token

    res = requests.get(base_endpoint, headers=headers, params=params)
    if res.status_code != 200:
        break

    data = res.json()
    all_documents.extend(data.get("documents", []))
    next_page_token = data.get("nextPageToken")
    if not next_page_token:
        break

print(f"Scanning {len(all_documents)} records for any field containing 'London'...\n")

found_count = 0
for doc in all_documents:
    fields = doc.get("fields", {})
    doc_id = doc["name"].split("/")[-1]
    title = fields.get("title", {}).get("stringValue", "Untitled")
    
    # Check country field specifically
    country_val = fields.get("country", {}).get("stringValue", "")
    
    # Check whole document dump
    doc_dump = json.dumps(fields).lower()
    
    if "london" in doc_dump:
        found_count += 1
        print(f"📌 Found match #{found_count}: '{title}' ({doc_id})")
        print(f"   - Current 'country' field: '{country_val}'")
        print(f"   - Raw fields dump: {json.dumps(fields, indent=2)}\n")

if found_count == 0:
    print("No records found containing 'London' in any field.")