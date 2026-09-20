import json

with open(
    "config/afro-discovery-system-firebase-adminsdk-fbsvc-e7f28e7a4c.json",
    "r"
) as f:

    data = json.load(f)

print("\nPROJECT ID:")
print(data["project_id"])

print("\nCLIENT EMAIL:")
print(data["client_email"])
