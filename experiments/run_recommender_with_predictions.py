import json
from pathlib import Path

from recommender.skill_extractor import load_skill_catalog
from recommender.recommend_issues import recommend_for_developer

PRED = Path("experiments/output/predicciones_test.json")
SKILLS = Path("recommender/skills.json")

def main():
    issues = json.loads(PRED.read_text(encoding="utf-8"))
    catalog = load_skill_catalog(SKILLS)

    developer_skills = {
        "python": 1.0,
        "data": 0.8,
        "ml": 0.6,
        "nlp": 0.6,
        "git": 0.4,
        "testing": 0.3
    }

    recs = recommend_for_developer(issues, developer_skills, catalog, top_k=10)

    print("\n=== TOP RECOMENDACIONES (con labels predichas) ===")
    for i, r in enumerate(recs, 1):
        print(f"\n#{i} Issue {r.issue_id} | score={r.score:.2f}")
        print(f"   {r.reason}")
        print(f"   predicted_labels: {r.predicted_labels}")

if __name__ == "__main__":
    main()
