import json
import csv
import os
import re

# ============================================
# 📌 RUTAS ABSOLUTAS BASADAS EN LA RAÍZ DEL PROYECTO
# ============================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "data", "raw", "issues_raw.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "corpus.csv")


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)        # URLs
    text = re.sub(r"`.*?`", "", text)          # código inline
    text = re.sub(r"[^a-z\s]", " ", text)      # símbolos
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_corpus():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        issues = json.load(f)

    output_dir = os.path.dirname(OUTPUT_FILE)
    os.makedirs(output_dir, exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["issue_id", "text", "labels"])

        for issue in issues:
            text = f"{issue['title']} {issue['body']}"
            text = clean_text(text)
            labels = ";".join(issue.get("labels", []))

            writer.writerow([
                issue["issue_id"],
                text,
                labels
            ])

    print(f"[OK] Corpus created at {OUTPUT_FILE}")


if __name__ == "__main__":
    build_corpus()
