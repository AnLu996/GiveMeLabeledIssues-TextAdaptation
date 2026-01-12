from flask import Flask, request, jsonify
from load_corpus import load_corpus
from collections import Counter
import re
from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": "*"}}
)
df = load_corpus()

@app.route("/")
def health_check():
    return {"status": "Backend up", "issues_loaded": len(df)}

# --------------------------------------------------
# 🔍 SEARCH ENDPOINT
# --------------------------------------------------
@app.route("/search", methods=["GET"])
def search():
    """
    Query params:
    - q: texto libre
    - labels: lista de labels (?labels=PRIORITY&labels=NEWCOMER)
    - mode: 'or' | 'and'
    """
    query = request.args.get("q", "").lower()
    labels = request.args.getlist("labels")
    mode = request.args.get("mode", "or")

    selected_labels = set(labels)

    def match(row):
        # Texto
        text_match = query in row["text"].lower() if query else True

        # Labels
        if not selected_labels:
            label_match = True
        elif mode == "and":
            label_match = selected_labels.issubset(row["label_set"])
        else:  # OR
            label_match = len(selected_labels & row["label_set"]) > 0

        return text_match and label_match

    results = df[df.apply(match, axis=1)]

    return jsonify({
        "total_results": len(results),
        "query": query,
        "labels": labels,
        "mode": mode,
        "results": results[["issue_id", "labels", "text"]].to_dict(orient="records")
    })


@app.route("/search_by_labels")
def search_by_labels():
    labels_param = request.args.get("labels", "")
    if not labels_param:
        return jsonify([])

    selected = labels_param.split(",")

    filtered = df[df["labels"].apply(
        lambda x: any(label in x for label in selected)
    )]

    return filtered.head(20).to_dict(orient="records")



@app.route("/available_queries", methods=["GET"])
def available_queries():
    """
    Devuelve las categorías disponibles basadas en los labels del corpus.
    Pensado para checkbox en frontend.
    """
    labels_series = df["labels"].dropna()

    all_labels = set()

    for label_str in labels_series:
        labels = [l.strip().lower() for l in label_str.split(";") if l.strip()]
        for l in labels:
            # Opcional: filtrar labels no semánticos
            # if l not in {"priority", "newcomer"}:
            all_labels.add(l)

    return jsonify(sorted(all_labels))



# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
    

