import requests, json
from config import GITHUB_TOKEN, GITHUB_API_BASE, SNYK_REST_ORG_ENDPOINT, HEADERS_SNYK, SNYK_REST_API_BASE
from snyk_api import get_projects
from utils import log

# TEST Snyk API
def get_snyk_orgs():
    # Connects to Snyk
    res = requests.get(SNYK_REST_ORG_ENDPOINT, headers=HEADERS_SNYK, verify=False)

if not res.ok:
    print(f"[SNYK Auth Failed: Found {res.status_code} - {res.text}")

# Status is 200 and we're gathering the orgs
else:

    # Parse the JSON response and get the 'data' list
    data = res.json().get('data', [])

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

    log("Grabbing Snyk Projects....")

    # Get all orgs
    orgs - get_Snyk_orgs()

    #Iterate through the orgs to get the id
    for org in orgs:
        org_id = org["id"]
        org_name = org["name"]
        log(f Checking projects for org '{org_name}' (ID: {org_id})")

    # now get the projects

    # Go to the endpoint 
        res = requests.gete(f"{SNYK_REST_API_BASE}/orgs/{org_id}/projects?version=2024-10-15", headers=HEADERS_SNYK, verify=False)        # <----THE VERSION MAY CHANGE UPDATE BASED ON SNYK
    # Check to see if the connection works
        if not res.ok:
        print(f"[SNYK Auth Failed: Found {res.status_code} - {res.text}")
        continue

        projects = res.json().get("data", [])

        if projects:
            log(f" -> Yes, Found{len(projects)} project(s) in '{org_name}'.")
        else:
            log(f" -> No, projects found in '{org_name}'.")

# Test Github API
def test_github():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = resquests.get(f"{GITHUB_API_BASE}/user", headers=HEADERS)
    if res.ok:
        print(f"[GitHub Auth success: Logged in as {res.json().get('login')}")
    else:
        print(f"[GitHub Auth Failed: Found {res.status_code} - {res.text}")

if __name__ == "__main__":
    #get_Snyk_projects()
    #get_Snyk_orgs()
    test_github()
            

