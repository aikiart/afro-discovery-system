import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore


class FirebaseService:

    def __init__(self):

        cred = credentials.Certificate(
            "config/afro-discovery-system-firebase-adminsdk-fbsvc-e7f28e7a4c.json"
        )

        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def save_resource(self, data):

        self.db.collection(
            "resources"
        ).add(data)

        print(
            "Resource saved to Firebase."
        )