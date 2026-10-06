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

print(f"Scanning {len(all_documents)} documents for country = 'London'...")

updated_count = 0
for doc in all_documents:
    fields = doc.get("fields", {})
    country_val = fields.get("country", {}).get("stringValue", "").strip()

    if country_val.lower() == "london":
        doc_name = doc["name"]
        
        # Patch field 'country' to 'England' using updateMask so other fields stay intact
        patch_url = f"https://firestore.googleapis.com/v1/{doc_name}?updateMask.fieldPaths=country"
        
        # Update existing fields dictionary
        fields["country"] = {"stringValue": "England"}
        payload = {"fields": fields}
        
        patch_res = requests.patch(patch_url, headers=headers, json=payload)
        
        if patch_res.status_code in (200, 201):
            doc_id = doc_name.split("/")[-1]
            title = fields.get("title", {}).get("stringValue", "Untitled")
            print(f"  ✅ Reassigned '{title}' ({doc_id}) -> Country: England")
            updated_count += 1
        else:
            print(f"  ⚠️ Failed to update {doc_name}: {patch_res.status_code} {patch_res.text}")

print(f"\nUpdate complete. Total documents reassigned to England: {updated_count}")