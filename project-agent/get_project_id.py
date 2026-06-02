import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("GITLAB_PERSONAL_ACCESS_TOKEN")
headers = {"PRIVATE-TOKEN": token}

url = "https://gitlab.com/api/v4/projects?owned=true"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    projects = response.json()
    print(f"Found {len(projects)} owned projects:")
    for p in projects:
        print(f"Found Project: {p['path_with_namespace']} (ID: {p['id']})")
else:
    print(f"Error: {response.status_code} - {response.text}")
