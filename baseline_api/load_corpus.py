import pandas as pd

def load_corpus(path="../data/processed/corpus.csv"):
    df = pd.read_csv(path)

    df["labels"] = df["labels"].fillna("")
    df["text"] = df["text"].fillna("")
    df["label_set"] = df["labels"].apply(
        lambda x: set(x.split("|")) if x else set()
    )

    print(f"[INFO] Issues encontrados en CSV: {len(df)}")
    print("[OK] JabRef cargado correctamente")

    return df
