import requests
import time

# Tokens for authenticating with Snyk and GitHub
SNYK_TOKEN = "your_snyk_api_token_here"           # <-- replace with your Snyk token
GITHUB_TOKEN = "your_github_pat_here"             # <-- replace with your GitHub PAT

# Base API endpoints
SNYK_API_BASE = "https://api.snyk.io/v1"

# Request headers for each API
HEADERS_SNYK = {
    "Authorization": f"token {SNYK_TOKEN}",
    "Content-Type": "application/json"
}

HEADERS_GITHUB = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# Where we log script activity
LOG_FILE = "snyk_pr_check_update_log.txt"

# Name of the PR check we want to modify
PR_CHECK_NAME = "snyk/code"


# Logging helper to print + save to file
def log(message):
    with open(LOG_FILE, "a") as log_file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")
    print(message)


# Get all orgs the Snyk token has access to
def get_snyk_orgs():
    response = requests.get(f"{SNYK_API_BASE}/orgs", headers=HEADERS_SNYK)
    return response.json().get("orgs", [])


# Get all projects for a given Snyk org ID
def get_snyk_projects(org_id):
    response = requests.get(f"{SNYK_API_BASE}/org/{org_id}/projects", headers=HEADERS_SNYK)
    return response.json().get("projects", [])


# Get the default branch of a GitHub repo
def get_default_branch(repo_full_name):
    response = requests.get(f"https://[INSERT_ENTERPRISE_DOMAIN_NAME].github.com/repos/{repo_full_name}", headers=HEADERS_GITHUB)  # < -- This can also be used for github, just change the url
    if response.status_code == 200:
        return response.json().get("default_branch")
    return None


# Get current branch protection rules from GitHub
def get_branch_protection(repo_full_name, branch):
    url = f"ttps://[INSERT_ENTERPRISE_DOMAIN_NAME].github.com/repos/{repo_full_name}/branches/{branch}/protection"
    response = requests.get(url, headers=HEADERS_GITHUB)
    if response.status_code == 200:
        return response.json()
    return None


# Update PR check requirement: make 'snyk/code' optional
def update_pr_check(repo_full_name, branch, existing_protection):
    # Get the required status checks block
    required_checks = existing_protection.get("required_status_checks", {})
    if not required_checks:
        log(f"{repo_full_name}: No required checks on branch {branch}. Skipping.")
        return

    # Get current list of required PR checks
    contexts = required_checks.get("contexts", [])
    if PR_CHECK_NAME not in contexts:
        log(f"{repo_full_name}: '{PR_CHECK_NAME}' not found in required checks.")
        return

    # Remove 'snyk/code' from required list but keep others
    updated_contexts = [check for check in contexts if check != PR_CHECK_NAME]

    # Prepare the new branch protection payload
    new_payload = {
        "required_status_checks": {
            "strict": required_checks.get("strict", False),
            "contexts": updated_contexts
        },
        "enforce_admins": existing_protection.get("enforce_admins", {}).get("enabled", False),
        "required_pull_request_reviews": existing_protection.get("required_pull_request_reviews", None),
        "restrictions": existing_protection.get("restrictions", None),
    }

    # Make the update request
    url = f"https://api.github.com/repos/{repo_full_name}/branches/{branch}/protection"
    response = requests.put(
        url,
        headers={**HEADERS_GITHUB, "Accept": "application/vnd.github.luke-cage-preview+json"},
        json=new_payload
    )

    # Log result
    if response.status_code == 200:
        log(f"{repo_full_name}: Successfully set '{PR_CHECK_NAME}' as optional.")
    else:
        log(f"{repo_full_name}: Failed to update PR check - {response.status_code} - {response.text}")


# Main script logic
def main():
    # Step 1: Get all Snyk organizations
    orgs = get_snyk_orgs()

    for org in orgs:
        org_id = org.get("id")
        org_name = org.get("name")

        # Step 2: Get all projects in the Snyk org
        projects = get_snyk_projects(org_id)

        for project in projects:
            proj_name = project.get("name")

            # Step 3: Estimate GitHub repo name from project name
            # NOTE: You might need to normalize or map this if names differ
            repo_full_name = proj_name.strip()

            # Step 4: Get the default branch of the repo
            branch = get_default_branch(repo_full_name)
            if not branch:
                log(f"{repo_full_name}: Could not determine default branch. Skipping.")
                continue

            # Step 5: Get current branch protection rules
            protection = get_branch_protection(repo_full_name, branch)
            if not protection:
                log(f"{repo_full_name}: No protection rules found. Skipping.")
                continue

            # Step 6: Update the PR check to be optional
            update_pr_check(repo_full_name, branch, protection)


# Run the script
if __name__ == "__main__":
    main()
