import os
from typing import Any, Dict, List, Set
import firebase_admin
from firebase_admin import credentials, firestore


class DatabaseAgent:
    """Agent responsible for writing, reading, and cleaning up platform records in Firebase Firestore."""

    def __init__(self, service_account_path: str = None):
        if service_account_path is None:
            service_account_path = os.path.join("config", "serviceAccountKey.json")

        if not os.path.exists(service_account_path):
            raise FileNotFoundError(
                f"Firebase service account key not found at '{service_account_path}'. "
                "Please ensure your serviceAccountKey.json is placed in the 'config/' folder."
            )

        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def sanitize_doc_id(self, url: str) -> str:
        """Sanitizes URL to produce a safe document ID."""
        return (
            url.replace("https://", "")
            .replace("http://", "")
            .replace("/", "_")
            .replace("?", "_")
            .replace("#", "_")
            .replace(".", "_")
        )

    def get_existing_urls(self, collection_name: str = "afro_centric_apps") -> Set[str]:
        """Fetches all existing site URLs from Firestore to skip duplicates."""
        docs = self.db.collection(collection_name).select(["url"]).stream()
        existing_urls = set()
        for doc in docs:
            data = doc.to_dict()
            if data and "url" in data:
                existing_urls.add(data["url"].rstrip("/"))
        return existing_urls

    def delete_record_by_url(self, url: str, collection_name: str = "afro_centric_apps") -> bool:
        """Removes an invalid or dead site record from Firestore."""
        doc_id = self.sanitize_doc_id(url)
        doc_ref = self.db.collection(collection_name).document(doc_id)
        if doc_ref.get().exists:
            doc_ref.delete()
            print(f"🗑️ Removed dead link from Firestore: {url}")
            return True
        return False

    def save_records(
        self, records: List[Dict[str, Any]], collection_name: str = "afro_centric_apps"
    ) -> int:
        """Saves or updates records in Firestore."""
        collection_ref = self.db.collection(collection_name)
        saved_count = 0

        for record in records:
            url = record.get("url", "")
            if not url or record.get("error"):
                continue

            doc_id = self.sanitize_doc_id(url)
            doc_ref = collection_ref.document(doc_id)
            doc_ref.set(record, merge=True)
            saved_count += 1

        print(
            f"✅ Successfully upserted {saved_count} new records into Firestore collection '{collection_name}'."
        )
        return saved_count