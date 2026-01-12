import pandas as pd
import os

def load_corpus(path=None):
    # Si no se pasa path, calcularlo relativo a la ubicación de ESTE script
    if path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, "data", "processed", "corpus.csv")

    print(f"[INFO] Cargando corpus desde: {path}")
    df = pd.read_csv(path)

    df["labels"] = df["labels"].fillna("")
    df["text"] = df["text"].fillna("")
    # Crear set de labels (usando ; como separador)
    df["label_set"] = df["labels"].apply(
        lambda x: set(x.split(";")) if x else set()
    )

    print(f"[INFO] Issues encontrados en CSV: {len(df)}")
    print("[OK] Corpus cargado correctamente")

    return df
