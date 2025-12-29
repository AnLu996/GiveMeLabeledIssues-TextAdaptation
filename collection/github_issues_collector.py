import requests
import json

OWNER = "jabref"
REPO = "jabref"
MAX_ISSUES = 300

def collect_issues():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    params = {
        "state": "closed",
        "per_page": 100
    }

    issues = []
    page = 1

    while len(issues) < MAX_ISSUES:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            break

        for issue in data:
            if "pull_request" not in issue:
                issues.append({
                    "id": issue["number"],
                    "title": issue["title"],
                    "body": issue["body"] or ""
                })

        page += 1

    return issues

if __name__ == "__main__":
    issues = collect_issues()
    with open("data/raw/issues.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2)
