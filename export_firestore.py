import json

from services.firebase_service import FirebaseService

firebase = FirebaseService()

docs = (
    firebase.db
    .collection("resources")
    .stream()
)

results = []

for doc in docs:

    record = doc.to_dict()

    record["firebase_id"] = doc.id

    results.append(record)

with open(
    "data/export.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=4,
        ensure_ascii=False
    )

print(
    f"Exported {len(results)} records."
)