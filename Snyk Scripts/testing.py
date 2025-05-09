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
