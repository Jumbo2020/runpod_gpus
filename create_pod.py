import os
import requests
import json
import traceback
import sys

print("=== RUNPOD DEBUG START ===")
sys.stdout.flush()

print("ENVIRONMENT VARIABLES:")
print(json.dumps(dict(os.environ), indent=2))
sys.stdout.flush()

try:
    # קבלת מפתח ה-API מהסביבה
    API_KEY = os.getenv("RUNPOD_KEY")
    if not API_KEY:
        raise Exception("❌ RUNPOD_KEY not found in environment variables.")
    sys.stdout.flush()

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
        }
      }
    }
    """

    # ערכי קלט חיוניים לפי הדוקומנטציה
    variables = {
        "input": {
            "name": "github-pod",
            "imageName": "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
            "gpuTypeId": "NVIDIA RTX A6000",  # ודא שזה מזהה חוקי, אפשר לבדוק עם query ל-gpuTypes
            "cloudType": "SECURE",
            "gpuCount": 1,
            "containerDiskInGb": 20,
            "volumeInGb": 40,
            "minVcpuCount": 2,
            "minMemoryInGb": 15,
            "volumeMountPath": "/workspace",
            "dockerArgs": "",
            "ports": "8888/http",
            "env": [
                {"key": "JUPYTER_PASSWORD", "value": "yourpassword"}
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # שליחת הבקשה
    response = requests.post(URL, headers=headers, json={"query": query, "variables": variables})

    print("Status code:", response.status_code)
    sys.stdout.flush()
    print("Raw response text:")
    print(response.text)
    sys.stdout.flush()

    try:
        data = response.json()
        print("\nParsed JSON response:")
        print(json.dumps(data, indent=2))
        sys.stdout.flush()
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        data = None
        sys.stdout.flush()

    if data and "errors" in data:
        print("\nGraphQL errors:")
        print(json.dumps(data["errors"], indent=2))
        sys.stdout.flush()

    if data and "data" in data and data["data"] and data["data"].get("podFindAndDeployOnDemand"):
        pod_data = data["data"]["podFindAndDeployOnDemand"]
        print("\u2705 Pod Created:")
        print(json.dumps(pod_data, indent=2))
        with open("pod_output.json", "w") as f:
            json.dump(pod_data, f, indent=2)
        sys.stdout.flush()
    else:
        print("\u274C Pod was not created. See above for details.")
        sys.stdout.flush()

    print("\u2139\ufe0f Endpoint URL not available via GraphQL. Use RunPod console to access.")
    sys.stdout.flush()

except Exception as e:
    print(f"UNCAUGHT ERROR: {e}")
    traceback.print_exc()
    sys.stdout.flush()
