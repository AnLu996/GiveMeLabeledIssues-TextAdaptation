from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from recommender.skill_extractor import SkillMatch, extract_skills


@dataclass
class IssueRecommendation:
    issue_id: str
    score: float
    matched_skills: List[str]
    predicted_labels: List[str]
    reason: str


LABEL_TO_SKILL_BONUS = {
    # bonuses "suaves" para priorizar issues según tu propuesta
    "NEWCOMER": {"docs": 0.6, "testing": 0.4},
    "DEVELOPMENT": {"ml": 0.3, "nlp": 0.3, "backend": 0.2},
    "COMPONENT": {"backend": 0.2, "frontend": 0.2, "data": 0.2},
    "PRIORITY": {}  # no es habilidad, pero podrías usarlo como penalización si el dev es junior
}


def recommend_for_developer(
    issues: List[dict],
    developer_skills: Dict[str, float],
    skill_catalog: Dict[str, List[str]],
    top_k: int = 10
) -> List[IssueRecommendation]:
    """
    issues: lista de dicts con al menos:
      - issue_id
      - text
      - predicted_labels (list[str])  (puede venir del modelo o estar vacío)
    developer_skills: {"python": 1.0, "ml": 0.7, ...} niveles [0..1] o pesos
    """
    recs: List[IssueRecommendation] = []

    for it in issues:
        issue_id = str(it.get("issue_id", ""))
        text = it.get("text", "") or ""
        pred_labels = it.get("predicted_labels", []) or []

        skill_matches = extract_skills(text, skill_catalog)
        issue_skills = {m.skill: m.score for m in skill_matches}

        # score base: coincidencia skills(dev) * score(skill en issue)
        score = 0.0
        matched = []
        for sk, dev_w in developer_skills.items():
            if sk in issue_skills:
                score += float(dev_w) * float(issue_skills[sk])
                matched.append(sk)

        # bonus por etiquetas (si existen)
        for lb in pred_labels:
            bonus_map = LABEL_TO_SKILL_BONUS.get(lb, {})
            for sk, b in bonus_map.items():
                if sk in developer_skills:
                    score += b * float(developer_skills[sk])

        if score <= 0:
            continue

        reason = f"Match skills: {', '.join(matched[:6])}" if matched else "Matched by label bonuses"
        recs.append(
            IssueRecommendation(
                issue_id=issue_id,
                score=score,
                matched_skills=matched,
                predicted_labels=pred_labels,
                reason=reason,
            )
        )

    recs.sort(key=lambda r: r.score, reverse=True)
    return recs[:top_k]
