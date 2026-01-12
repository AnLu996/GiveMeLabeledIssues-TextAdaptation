import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, hamming_loss, jaccard_score, classification_report

from sentence_transformers import SentenceTransformer


CORPUS = Path("data/processed/corpus.csv")


def parse_labels(s):
    if pd.isna(s):
        return []
    if isinstance(s, list):
        return s
    txt = str(s).strip()
    if not txt:
        return []
    # tu formato real: "A;B;C"
    if ";" in txt:
        return [x.strip() for x in txt.split(";") if x.strip()]
    # fallback
    if "|" in txt:
        return [x.strip() for x in txt.split("|") if x.strip()]
    if "," in txt:
        return [x.strip() for x in txt.split(",") if x.strip()]
    return [txt]


def main():
    df = pd.read_csv(CORPUS)
    X = df["text"].astype(str)
    y_list = df["labels"].apply(parse_labels)

    mlb = MultiLabelBinarizer()
    Y = mlb.fit_transform(y_list)
    label_names = list(mlb.classes_)

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42
    )

    print("[INFO] Cargando modelo de embeddings...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("[INFO] Generando embeddings...")
    emb_train = model.encode(X_train.tolist(), show_progress_bar=True, normalize_embeddings=True)
    emb_test = model.encode(X_test.tolist(), show_progress_bar=True, normalize_embeddings=True)

    clf = OneVsRestClassifier(
        LogisticRegression(max_iter=2000)
    )

    print("[INFO] Entrenando clasificador...")
    clf.fit(emb_train, Y_train)

    print("[INFO] Prediciendo...")
    Y_pred = clf.predict(emb_test)

    print("\n=== MÉTRICAS (BERT embeddings + OVR LogReg) ===")
    print("micro F1:", f1_score(Y_test, Y_pred, average="micro", zero_division=0))
    print("macro F1:", f1_score(Y_test, Y_pred, average="macro", zero_division=0))
    print("micro precision:", precision_score(Y_test, Y_pred, average="micro", zero_division=0))
    print("micro recall:", recall_score(Y_test, Y_pred, average="micro", zero_division=0))
    print("hamming_loss:", hamming_loss(Y_test, Y_pred))
    print("jaccard_micro:", jaccard_score(Y_test, Y_pred, average="micro", zero_division=0))

    print("\n=== REPORTE ===")
    print(classification_report(Y_test, Y_pred, target_names=label_names, zero_division=0))


if __name__ == "__main__":
    main()
