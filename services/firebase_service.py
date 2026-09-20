import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore


class FirebaseService:

    def __init__(self):

        if not firebase_admin._apps:

            cred = credentials.Certificate(
                "config/afro-discovery-system-firebase-adminsdk-fbsvc-e7f28e7a4c.json"
            )

            firebase_admin.initialize_app(
                cred
            )

        self.db = firestore.client()

    def url_exists(self, url):

        docs = (
            self.db.collection(
                "resources"
            )
            .where(
                "url",
                "==",
                url
            )
            .stream()
        )

        return any(docs)

    def save_resource(self, data):

        if self.url_exists(
            data["url"]
        ):

            print(
                f"Skipping duplicate: {data['url']}"
            )

            return

        self.db.collection(
            "resources"
        ).add(data)

        print(
            "Resource saved to Firebase."
        )