from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


WORD_RE = re.compile(r"[a-z0-9\-\.]+")


@dataclass
class SkillMatch:
    skill: str
    score: float
    hits: List[str]


def load_skill_catalog(path: Path) -> Dict[str, List[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    # normalizar keywords a minúsculas
    return {k: [w.lower() for w in v] for k, v in data.items()}


def extract_skills(text: str, catalog: Dict[str, List[str]]) -> List[SkillMatch]:
    """
    Baseline: matching por keywords con scoring simple.
    - score = número de keywords encontradas (con pequeño bonus por frases exactas)
    """
    t = (text or "").lower()
    tokens = set(WORD_RE.findall(t))

    matches: List[SkillMatch] = []
    for skill, kws in catalog.items():
        hits: List[str] = []
        score = 0.0

        for kw in kws:
            kw_l = kw.lower().strip()
            if not kw_l:
                continue

            # keyword multi-palabra: buscamos substring
            if " " in kw_l:
                if kw_l in t:
                    hits.append(kw)
                    score += 2.0
            else:
                if kw_l in tokens:
                    hits.append(kw)
                    score += 1.0

        if score > 0:
            matches.append(SkillMatch(skill=skill, score=score, hits=hits))

    matches.sort(key=lambda m: m.score, reverse=True)
    return matches


def top_skills(text: str, catalog: Dict[str, List[str]], k: int = 5) -> List[SkillMatch]:
    return extract_skills(text, catalog)[:k]
