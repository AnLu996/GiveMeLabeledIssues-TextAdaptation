import json
from pathlib import Path

from recommender.skill_extractor import top_skills, load_skill_catalog
from recommender.recommend_issues import recommend_for_developer

PRED = Path("experiments/output/predicciones_test.json")
SKILLS = Path("recommender/skills.json")

OUT = Path("experiments/output")
OUT.mkdir(parents=True, exist_ok=True)


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

    recs_out = []
    for r in recs:
        issue = next((it for it in issues if str(it.get("issue_id")) == str(r.issue_id)), None)
        if issue is None:
            continue

        skills = top_skills(issue.get("text", ""), catalog, k=8)

        recs_out.append({
            "issue_id": r.issue_id,
            "score": round(r.score, 4),
            "predicted_labels": r.predicted_labels,
            "matched_skills": r.matched_skills,
            "skills_detected": [{"skill": s.skill, "score": s.score, "hits": s.hits} for s in skills],
            "reason": r.reason
        })

    (OUT / "recomendaciones.json").write_text(
        json.dumps(recs_out, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"\n[OK] Guardado: {OUT/'recomendaciones.json'}")


if __name__ == "__main__":
    main()
