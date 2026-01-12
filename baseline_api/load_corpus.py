import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GiveMeLabeledIssues.settings")
django.setup()

from GiveMeLabeledIssues.models import JabRefIssue

CSV_PATH = "../data/processed/corpus.csv"


# Mapeo de labels del CSV → columnas del modelo
LABEL_MAP = {
    "📌 Pinned": "Pinned",
    "📍 Assigned": "Assigned",
    "component: jabsrv": "Data_Structure",
    "component: entry-editor": "UI",
    "component: preferences": "UI",
    "dev: ci-cd": "DevOps",
    "good first issue": "Util",
    "good second issue": "Util",
    "status: depends-on-external": "Logic",
}


def load_jabref():
    df = pd.read_csv(CSV_PATH)

    print(f"[INFO] Issues encontrados en CSV: {len(df)}")

    for _, row in df.iterrows():
        labels = []
        if pd.notna(row["labels"]):
            labels = [l.strip() for l in row["labels"].split(";")]

        issue = JabRefIssue(
            issueNumber=int(row["issue_id"]),
            issueTitle=row["text"][:200],
            issueText=row["text"],
            issueLabels=row["labels"] if pd.notna(row["labels"]) else "",
            # Inicializamos TODO en False
            Util=False,
            NLP=False,
            APM=False,
            Network=False,
            DB=False,
            Interpreter=False,
            Logging=False,
            Data_Structure=False,
            i18n=False,
            DevOps=False,
            Logic=False,
            Microservices=False,
            Test=False,
            Search=False,
            IO=False,
            UI=False,
            Parser=False,
            Security=False,
            App=False,
        )

        # Activar flags según labels
        for label in labels:
            if label in LABEL_MAP:
                setattr(issue, LABEL_MAP[label], True)

        issue.save()

    print("[OK] JabRef cargado correctamente")


if __name__ == "__main__":
    load_jabref()
