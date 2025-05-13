import requests, json
from config import SNYK_TOKEN, GITHUB_TOKEN, SNYK_API_BASE, GITHUB_API_BASE, SNYK_REST_API_BASE, HEADERS_SNYK
from snyk_api import get_orgs, get_projects
from utils import log

# Test Snyk API
def get_snyk_orgs():
    # Connects to Snyk
    res = requests.get(SNYK_REST_ORG_ENDPOINT, headers=HEADERS_SNYK, verify=False)

    if not res.ok:
        print(f" {SNYK Auth failed: Found {res.status_code} - {res.text}")

    # Status is 200, so we get the orgs
    else:
        # Step 1: Parse the JSON response and get the 'data' list
        data = res.json.get('data', [])

        # Prepare a list to hold simplified org dictionaries
        orgs = []

        # Iterate over each org object in the 'data' array
        for item in data:
            # Extract the org ID (top level field)
            org_id = item.get("id")

            # Extract the org name (nested inside 'attributes')
            org_name = item.get("attributes", {}).get("name")

            # Only add to the list if both ID and name exist
            if org_id and org_name:
                orgs.append({
                    "id": org_id,
                    "name": org_name
                })

        # Return clean list of orgs
        return orgs


def get_Snyk_projects():
    log("Grabbing Snyk Projects...")

    # Get all orgs
    orgs = get_Snyk_orgs()

    # Now get the projects

    # Step 1: Go to the endpoint
    rest = requests.get(f"{Snyk_REST_API_BASE}/orgs/{org_id}/projects?version=2024-10-15", headers=HEADERS_SNYK, verify=False)

    # Check to see if the connection works
    if not res.ok:
        print(f"Snyk Auth Failed: Found {res.status_code} - {res.text}")

    else:
        # Step 1: Parse the JSON response and get the 'data' list
        data = res.json().get('name', [])
        print(data)



# Test Github API
def test_github():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(f"{GITHUB_API_BASE}/user", headers=headers)
    if res.ok:
        print(f"[GitHub Auth Success: Logged in as {res.json().get('login')}")
    else:
        print(f"[GitHub Auth Failed: Found {res.status_code} - {res.text}")

if __name__ == "__main__":
    get_Snyk_projects()
            
