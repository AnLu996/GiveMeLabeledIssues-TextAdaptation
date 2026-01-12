from pathlib import Path
import pandas as pd

from recommender.skill_extractor import load_skill_catalog, top_skills
from recommender.recommend_issues import recommend_for_developer


CORPUS = Path("data/processed/corpus.csv")
SKILLS = Path("recommender/skills.json")


def main():
    df = pd.read_csv(CORPUS)
    catalog = load_skill_catalog(SKILLS)

    # Perfil de ejemplo (puedes cambiarlo)
    developer_skills = {
        "python": 1.0,
        "data": 0.8,
        "ml": 0.6,
        "nlp": 0.6,
        "git": 0.4,
        "testing": 0.3
    }

    # Armamos lista de issues
    issues = []
    for _, row in df.iterrows():
        issues.append({
            "issue_id": row.get("issue_id", ""),
            "text": row.get("text", ""),
            "predicted_labels": []  # luego lo conectamos al modelo
        })

    recs = recommend_for_developer(issues, developer_skills, catalog, top_k=10)

    print("\n=== TOP RECOMENDACIONES ===")
    for i, r in enumerate(recs, 1):
        print(f"\n#{i} Issue {r.issue_id} | score={r.score:.2f}")
        print(f"   {r.reason}")
        if r.predicted_labels:
            print(f"   labels: {r.predicted_labels}")

    # También mostramos skills detectadas en el TOP 1
    if recs:
        top_issue = next(x for x in issues if str(x["issue_id"]) == recs[0].issue_id)
        skills = top_skills(top_issue["text"], catalog, k=8)
        print("\n=== Skills detectadas (TOP 1 issue) ===")
        for s in skills:
            print(f"- {s.skill}: score={s.score} hits={s.hits}")


if __name__ == "__main__":
    main()
