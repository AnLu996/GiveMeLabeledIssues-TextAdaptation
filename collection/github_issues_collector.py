import requests
import json
import os
import time

OWNER = "jabref"
REPO = "jabref"
MAX_ISSUES = 100  # GitHub permite máx. 100 por request sin paginación cursor

# 👉 RECOMENDADO: usar token por variable de entorno
# En PowerShell (una sola vez):
# setx GITHUB_TOKEN "tu_token_aqui"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"


def collect_issues():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    params = {
        "state": "closed",
        "per_page": MAX_ISSUES
    }

    response = requests.get(url, params=params, headers=HEADERS)

    # ---- VALIDACIÓN DE RESPUESTA ----
    if response.status_code != 200:
        print(f"[ERROR] GitHub API status {response.status_code}")
        print(response.json())
        return []

    data = response.json()

    if not isinstance(data, list):
        print("[ERROR] Unexpected response format:")
        print(data)
        return []

    issues = []

    for issue in data:
        # Ignorar Pull Requests
        if "pull_request" in issue:
            continue

        issues.append({
            "issue_id": issue.get("number"),
            "title": issue.get("title", ""),
            "body": issue.get("body") or "",
            "labels": [label["name"] for label in issue.get("labels", [])]
        })

    return issues


if __name__ == "__main__":
    issues = collect_issues()

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/issues_raw.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)

    print(f"[OK] Collected {len(issues)} issues")
