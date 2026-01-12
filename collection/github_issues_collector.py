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
MAX_ISSUES = 300  # GitHub permite máx. 100 por request sin paginación cursor

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
    Recolecta issues cerrados desde GitHub API (ignorando PRs) usando paginación.

    Returns:
        list: Lista de diccionarios con información de issues
    """
    print(f"[INFO] Conectando a GitHub API para {OWNER}/{REPO}...")
    print(f"[INFO] Objetivo: recolectar {MAX_ISSUES} issues cerrados (sin PRs) ...")

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

    issues = []
    prs_skipped_total = 0
    page = 1
    per_page = 100  # máximo permitido por GitHub

    while len(issues) < MAX_ISSUES:
        params = {
            "state": "closed",
            "per_page": per_page,
            "page": page
        }

        try:
            print(f"[INFO] Enviando petición GET a: {url} (page={page}, per_page={per_page})")
            response = requests.get(url, params=params, headers=HEADERS, timeout=30)

            remaining = response.headers.get("X-RateLimit-Remaining", "?")
            limit = response.headers.get("X-RateLimit-Limit", "?")
            print(f"[INFO] Límite de API: {remaining}/{limit} peticiones restantes")

            if response.status_code != 200:
                print(f"[ERROR] GitHub API retornó status {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"[ERROR] Detalles: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"[ERROR] Respuesta: {response.text[:200]}")
                break

            data = response.json()
            if not isinstance(data, list):
                print("[ERROR] Formato de respuesta inesperado (no es una lista).")
                break

            if len(data) == 0:
                print("[INFO] No hay más elementos (lista vacía). Terminando paginación.")
                break

            page_prs_skipped = 0
            page_issues_added = 0

            for item in data:
                if "pull_request" in item:
                    page_prs_skipped += 1
                    continue

                issues.append({
                    "issue_id": item.get("number"),
                    "title": item.get("title", ""),
                    "body": item.get("body") or "",
                    "labels": [label["name"] for label in item.get("labels", [])]
                })
                page_issues_added += 1

                if len(issues) >= MAX_ISSUES:
                    break

            prs_skipped_total += page_prs_skipped
            print(f"[OK] Página {page}: +{page_issues_added} issues (omitidos {page_prs_skipped} PRs). Total issues: {len(issues)}/{MAX_ISSUES}")

            page += 1
            time.sleep(0.2)  # pequeño delay para ser amable con la API

        except requests.exceptions.Timeout:
            print("[ERROR] Timeout al conectar con GitHub API")
            break
        except requests.exceptions.ConnectionError:
            print("[ERROR] Error de conexión. Verifica tu conexión a internet")
            break
        except Exception as e:
            print(f"[ERROR] Error inesperado: {str(e)}")
            import traceback
            traceback.print_exc()
            break

    print(f"[RESUMEN] Issues recolectados: {len(issues)} | PRs omitidos: {prs_skipped_total}")
    return issues

if __name__ == "__main__":
    issues = collect_issues()

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/issues_raw.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)

    print(f"[OK] Collected {len(issues)} issues")
