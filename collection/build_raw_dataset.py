import json
from github_issues_collector import collect_issues
from github_commits_collector import collect_commits

def build_dataset():
    issues = collect_issues()
    dataset = []

    for issue in issues:
        commits = collect_commits(issue["id"])
        dataset.append({
            "issue_id": issue["id"],
            "title": issue["title"],
            "body": issue["body"],
            "commit_messages": commits,
            "labels": issue["labels"]
        })

    with open("data/raw/issues_raw.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    build_dataset()
