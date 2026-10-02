from services.firebase_service import FirebaseService


class DatabaseAgent:

    def __init__(self):
        self.firebase = FirebaseService()

    def exists(self, url: str) -> bool:
        """Checks if a URL already exists in Firestore."""
        return self.firebase.url_exists(url)

    def save(self, data: dict):
        """Saves a scraped resource record to Firestore."""
        self.firebase.save_resource(data)