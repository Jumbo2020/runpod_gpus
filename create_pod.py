import os
import requests
import json

# קבלת מפתח ה-API מ-GitHub Secrets
API_KEY = os.getenv("RUNPOD_KEY")
if not API_KEY:
    raise Exception("❌ RUNPOD_KEY not found in environment variables.")

URL = "https://api.runpod.io/graphql"

# GraphQL query: יצירת Pod בסיסי
query = """
mutation podFindAndDeployOnDemand($input: PodFindAndDeployOnDemandInput!) {
  podFindAndDeployOnDemand(input: $input) {
    id
    name
    imageName
    costPerHr
    desiredStatus
    endpoint {
      id
      host
      targetPort
    }
  }
}
"""

# ערכי קלט חיוניים
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

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# שליחת הבקשה
response = requests.post(URL, headers=headers, json={"query": query, "variables": variables})

if response.status_code != 200:
    raise Exception(f"GraphQL request failed: {response.text}")

data = response.json()
pod_data = data["data"]["podFindAndDeployOnDemand"]

# הדפסה
print("\u2705 Pod Created:")
print(json.dumps(pod_data, indent=2))

# בניית URL מלא במידת הצורך
if pod_data.get("endpoint"):
    host = pod_data["endpoint"].get("host")
    port = pod_data["endpoint"].get("targetPort")
    if host and port:
        print(f"\ud83d\udd17 Full URL: http://{host}:{port}")

# שמירה לקובץ
with open("pod_output.json", "w") as f:
    json.dump(pod_data, f, indent=2)
