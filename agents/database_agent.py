from services.firebase_service import FirebaseService


class DatabaseAgent:

    def __init__(self):

        self.firebase = FirebaseService()

    def save(self, data):

        self.firebase.save_resource(
            data
        )