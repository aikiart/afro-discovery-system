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

print(f"Scanning {len(all_documents)} documents for location/country = 'London'...")

updated_count = 0
for doc in all_documents:
    fields = doc.get("fields", {})
    doc_name = doc["name"]
    title = fields.get("title", {}).get("stringValue", "Untitled")
    
    country_val = fields.get("country", {}).get("stringValue", "").strip()
    location_val = fields.get("location", {}).get("stringValue", "").strip()

    needs_update = False
    
    # Check if either field contains 'London'
    if country_val.lower() == "london":
        fields["country"] = {"stringValue": "England"}
        needs_update = True

    if location_val.lower() == "london":
        fields["location"] = {"stringValue": "England"}
        # If 'country' was blank or missing, standardize it as well
        if not fields.get("country", {}).get("stringValue"):
            fields["country"] = {"stringValue": "England"}
        needs_update = True

    if needs_update:
        # Patch both fields using updateMask
        patch_url = f"https://firestore.googleapis.com/v1/{doc_name}?updateMask.fieldPaths=country&updateMask.fieldPaths=location"
        payload = {"fields": fields}
        
        patch_res = requests.patch(patch_url, headers=headers, json=payload)
        
        if patch_res.status_code in (200, 201):
            doc_id = doc_name.split("/")[-1]
            print(f"  ✅ Reassigned '{title}' ({doc_id}) -> England")
            updated_count += 1
        else:
            print(f"  ⚠️ Failed to update {doc_id}: {patch_res.status_code}")

print(f"\nUpdate complete. Total documents reassigned: {updated_count}")