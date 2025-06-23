import os
import requests

# קח את המפתח מה־Secret של GitHub
API_KEY = os.getenv("RUNPOD_KEY")
if not API_KEY:
    raise Exception("❌ RUNPOD_KEY not found in environment variables.")

# GraphQL endpoint
URL = "https://api.runpod.io/graphql"

# GraphQL mutation לשיגור Pod
query = """
mutation podFindAndDeployOnDemand($input: PodFindAndDeployOnDemandInput!) {
  podFindAndDeployOnDemand(input: $input) {
    id
    name
    imageName
    costPerHr
    desiredStatus
    ipAddress {
      ip
    }
  }
}
"""

# ערכים בסיסיים ליצירת Pod
variables = {
    "input": {
        "name": "github-pod",
        "imageName": "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
        "gpuTypeId": "NVIDIA A100 80GB PCIe",
        "cloudType": "SECURE",
        "containerDiskInGb": 20,
        "volumeMountPath": "/workspace"
    }
}

# headers עם Authorization
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# שלח את הבקשה
response = requests.post(URL, headers=headers, json={"query": query, "variables": variables})

# בדוק תקינות
if response.status_code != 200:
    raise Exception(f"GraphQL request failed: {response.text}")

# הדפס תוצאה
data = response.json()
print("✅ Pod Created:")
print(data["data"]["podFindAndDeployOnDemand"])
