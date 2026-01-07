import requests

OWNER = "jabref"
REPO = "jabref"

def collect_commits(issue_number):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/events"
    response = requests.get(url)
    events = response.json()

    commit_messages = []

    for event in events:
        if event.get("event") == "referenced" and "commit_id" in event:
            commit_url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{event['commit_id']}"
            commit_data = requests.get(commit_url).json()
            commit_messages.append(commit_data["commit"]["message"])

    return commit_messages
