import requests, json
from config import SNYK_TOKEN, GITHUB_TOKEN, SNYK_API_BASE, GITHUB_API_BASE, SNYK_REST_API_BASE, HEADERS_SNYK
from snyk_api import get_orgs, get_projects
from utils import log

# TEST Snyk API
def test_snyk():
    res = requests.get(f"{SNYK_REST_API_BASE}/orgs?version=2024-10-15", headers=HEADERS_SNYK, verify=False)
   
    if not res.ok:
        print(f"[SNYK Auth Failed: Found {res.status_code} - {res.text}")

    # The STATUS is 200 and we're going to call the test_orgs_projects() method
    else:
       test_orgs_projects()

def test_orgs_projects():
    log("Testing connection to Snyk....")

    # Step 1: Get all orgs
    orgs = get_orgs()
    if not orgs:
        log("[ SNYK ] No organization found. Check your token.")
        return log (f"[ SNYK ] Found {len(orgs)} organization(s).")
    for org in orgs:
        log(f"Org: {org.get('name')} (ID: {org.get('id')}")
    
    # Step 2: Test pulling projects from the first org
    first_org = orgs[0]
    org_id = first_org.get('id')

    projects = get_projects(org_id)
    if not projects: 
        log(f" [ SNYK ] No projects found in organization {first_org.get('name')}")    
        return log(f"[ SNYK ] Found {len(projects)} project(s) in {first_org.get('name')}.")          
    for project in projects[:5]:
        # Limit to first 5 for quick display
        log(f"Project: {project.get('name')} (ID: {project.get('id')})")    

# Test Github API
def test_github():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(f"{GITHUB_API_BASE}/user", headers=headers)
    if res.ok:
        print(f"[GitHub Auth success: Logged in as {res.json().get('login')}")
    else:
       print(f"[GitHub Auth Failed: Found {res.status_code} - {res.text}")


if __name__ == "__main__":
   #test_orgs_projects()
   test_snyk()
