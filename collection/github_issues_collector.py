"""
GitHub Issues Collector
========================

Recolecta issues desde la API de GitHub para el repositorio especificado.
"""

import requests
import json
import os
import time

OWNER = "jabref"
REPO = "jabref"
MAX_ISSUES = 100  # GitHub permite máx. 100 por request sin paginación cursor

# 👉 RECOMENDADO: usar token por variable de entorno
# En PowerShell (una sola vez):
# setx GITHUB_TOKEN "tu_token_aqui"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"
    print("[INFO] Token de GitHub detectado en variable de entorno")
else:
    print("[ADVERTENCIA] No se encontró GITHUB_TOKEN. Las peticiones serán limitadas (60 req/hora)")


def collect_issues():
    """
    Recolecta issues cerrados desde GitHub API.
    
    Returns:
        list: Lista de diccionarios con información de issues
    """
    print(f"[INFO] Conectando a GitHub API para {OWNER}/{REPO}...")
    print(f"[INFO] Solicitando hasta {MAX_ISSUES} issues cerrados...")
    
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    params = {
        "state": "closed",
        "per_page": MAX_ISSUES
    }

    try:
        print(f"[INFO] Enviando petición GET a: {url}")
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        
        # Verificar límite de rate
        remaining = response.headers.get("X-RateLimit-Remaining", "?")
        limit = response.headers.get("X-RateLimit-Limit", "?")
        print(f"[INFO] Límite de API: {remaining}/{limit} peticiones restantes")

        # ---- VALIDACIÓN DE RESPUESTA ----
        if response.status_code != 200:
            print(f"[ERROR] GitHub API retornó status {response.status_code}")
            try:
                error_data = response.json()
                print(f"[ERROR] Detalles: {json.dumps(error_data, indent=2)}")
            except:
                print(f"[ERROR] Respuesta: {response.text[:200]}")
            return []

        data = response.json()
        print(f"[OK] Respuesta recibida: {len(data) if isinstance(data, list) else 'formato inesperado'} elementos")

        if not isinstance(data, list):
            print("[ERROR] Formato de respuesta inesperado (no es una lista):")
            print(json.dumps(data, indent=2)[:500])
            return []

        issues = []
        prs_skipped = 0

        print(f"[INFO] Procesando {len(data)} elementos de la respuesta...")
        for issue in data:
            # Ignorar Pull Requests
            if "pull_request" in issue:
                prs_skipped += 1
                continue

            issues.append({
                "issue_id": issue.get("number"),
                "title": issue.get("title", ""),
                "body": issue.get("body") or "",
                "labels": [label["name"] for label in issue.get("labels", [])]
            })

        print(f"[OK] {len(issues)} issues procesados (se omitieron {prs_skipped} Pull Requests)")
        return issues

    except requests.exceptions.Timeout:
        print("[ERROR] Timeout al conectar con GitHub API")
        return []
    except requests.exceptions.ConnectionError:
        print("[ERROR] Error de conexión. Verifica tu conexión a internet")
        return []
    except Exception as e:
        print(f"[ERROR] Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    issues = collect_issues()

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/issues_raw.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)

    print(f"[OK] Collected {len(issues)} issues")
