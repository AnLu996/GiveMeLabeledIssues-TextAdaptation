"""
Build Raw Dataset
=================

Construye el dataset crudo recolectando issues y commits desde GitHub.
"""

import json
import os
from github_issues_collector import collect_issues
from github_commits_collector import collect_commits


def build_dataset():
    """
    Construye el dataset crudo combinando issues y commits de GitHub.
    
    Proceso:
    1. Recolecta issues desde GitHub API
    2. Para cada issue, recolecta commits relacionados
    3. Guarda todo en data/raw/issues_raw.json
    """
    print("\n" + "="*80)
    print("🚀 CONSTRUYENDO DATASET CRUDO")
    print("="*80 + "\n")
    
    # Paso 1: Recolectar issues
    print("[PASO 1/3] Recolectando issues desde GitHub...")
    print("-" * 80)
    issues = collect_issues()
    
    if not issues:
        print("[ERROR] No se pudieron recolectar issues. Verifica tu conexión y token de GitHub.")
        return
    
    print(f"[OK] {len(issues)} issues recolectados exitosamente\n")
    
    # Paso 2: Recolectar commits para cada issue
    print(f"[PASO 2/3] Recolectando commits para {len(issues)} issues...")
    print("-" * 80)
    dataset = []
    
    for idx, issue in enumerate(issues, 1):
        issue_id = issue["issue_id"]
        issue_title = issue.get("title", "")[:50] + "..." if len(issue.get("title", "")) > 50 else issue.get("title", "")
        
        print(f"[{idx}/{len(issues)}] Procesando issue #{issue_id}: {issue_title}")
        
        try:
            commits = collect_commits(issue_id)
            print(f"        ✓ Encontrados {len(commits)} commits relacionados")
            
            dataset.append({
                "issue_id": issue_id,
                "title": issue["title"],
                "body": issue["body"],
                "commit_messages": commits,
                "labels": issue["labels"]
            })
        except Exception as e:
            print(f"        ✗ Error al recolectar commits: {str(e)}")
            # Continuar con el siguiente issue aunque falle este
            dataset.append({
                "issue_id": issue_id,
                "title": issue["title"],
                "body": issue["body"],
                "commit_messages": [],
                "labels": issue["labels"]
            })
    
    print(f"\n[OK] Procesados {len(dataset)} issues con sus commits\n")
    
    # Paso 3: Guardar dataset
    print("[PASO 3/3] Guardando dataset en disco...")
    print("-" * 80)
    
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "issues_raw.json")
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        # Calcular estadísticas
        total_commits = sum(len(item["commit_messages"]) for item in dataset)
        total_labels = sum(len(item["labels"]) for item in dataset)
        
        print(f"[OK] Dataset guardado exitosamente en: {output_file}")
        print(f"\n📊 ESTADÍSTICAS DEL DATASET:")
        print(f"   - Total de issues: {len(dataset)}")
        print(f"   - Total de commits recolectados: {total_commits}")
        print(f"   - Total de etiquetas: {total_labels}")
        print(f"   - Promedio de commits por issue: {total_commits/len(dataset):.2f}")
        print(f"   - Promedio de etiquetas por issue: {total_labels/len(dataset):.2f}")
        
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el dataset: {str(e)}")
        return
    
    print("\n" + "="*80)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("="*80 + "\n")


if __name__ == "__main__":
    build_dataset()
