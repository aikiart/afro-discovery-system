import os
import json
import hashlib
import urllib.request
import urllib.error


class FirebaseService:

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cert_path = os.path.join(base_dir, "serviceAccount.json")

        if not os.path.exists(cert_path):
            raise FileNotFoundError(f"Service account key not found at: {cert_path}")

        with open(cert_path, "r", encoding="utf-8") as f:
            self.credentials = json.load(f)

        self.project_id = self.credentials.get("project_id", "afro-discovery-system")
        self.collection_name = "afro_centric_apps"
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{self.project_id}/databases/(default)/documents/{self.collection_name}"

    def _get_doc_id(self, url: str) -> str:
        clean_url = url.strip().rstrip('/').lower()
        return hashlib.md5(clean_url.encode('utf-8')).hexdigest()

    def url_exists(self, url: str) -> bool:
        doc_id = self._get_doc_id(url)
        doc_url = f"{self.base_url}/{doc_id}"

        req = urllib.request.Request(doc_url, method="GET")
        try:
            # Direct HTTP GET with a strict 3-second timeout
            with urllib.request.urlopen(req, timeout=3) as response:
                return response.status == 200
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            print(f"  ⚠️ Firestore HTTP Error ({e.code}): {e.reason}")
            return False
        except Exception as e:
            print(f"  ⚠️ Firestore check error: {e}")
            return False

    def save_resource(self, data: dict):
        url = data.get("url")
        if not url:
            print("  ⚠️ Skipping save: Missing URL.")
            return

        doc_id = self._get_doc_id(url)
        doc_url = f"{self.base_url}/{doc_id}"

        # Format Firestore REST payload
        payload = {
            "fields": {
                "title": {"stringValue": data.get("title") or ""},
                "summary": {"stringValue": data.get("description") or data.get("summary") or "No description provided."},
                "url": {"stringValue": url},
                "category": {"stringValue": data.get("category", "Community")},
                "contactEmail": {"stringValue": data.get("contactEmail") or ""},
            }
        }

        json_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(doc_url, data=json_data, method="PATCH")
        req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status in (200, 201):
                    print(f"  ✅ Saved to Firestore via REST: {data.get('title') or url}")
        except Exception as e:
            print(f"  ❌ Error saving via REST: {e}")