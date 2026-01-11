"""
Build Corpus
============

Convierte el dataset crudo (JSON) en un corpus procesado (CSV) listo para ML.
"""

import json
import csv
import os
import re
from collections import Counter

# ============================================
# 📌 RUTAS ABSOLUTAS BASADAS EN LA RAÍZ DEL PROYECTO
# ============================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "data", "raw", "issues_raw.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "corpus.csv")

# ============================================
# ✅ FILTRO DE ETIQUETAS RARAS
# ============================================
MIN_LABEL_FREQ = 5  # recomendado para ~100 issues (multilabel)

def map_labels_to_groups(labels):
    """
    Agrupa labels de GitHub a categorías más útiles para backlog grooming.
    labels: lista de strings (labels originales)
    return: lista de categorías (strings)
    """
    labels_set = set(labels)
    groups = set()

    # PRIORIDAD / URGENCIA
    if "📌 Pinned" in labels_set or "📍 Assigned" in labels_set:
        groups.add("PRIORITY")

    # ONBOARDING / TAREAS PARA NUEVOS
    if any(l.startswith("good ") for l in labels_set):
        # más estricto si quieres:
        # if any(l in labels_set for l in ["good first issue","good second issue","good third issue"]):
        groups.add("NEWCOMER")

    # AGRUPACIÓN POR COMPONENTES
    if any(l.startswith("component:") for l in labels_set):
        groups.add("COMPONENT")

    # AGRUPACIÓN DE TAREAS DE DEV / MANTENIMIENTO
    if any(l.startswith("dev:") for l in labels_set):
        groups.add("DEVELOPMENT")

    # TAMAÑO
    #if any(l.startswith("size:") for l in labels_set):
    #    groups.add("SIZE")

    # ESTADO / BLOQUEOS
    #if any(l.startswith("status:") for l in labels_set):
    #    groups.add("STATUS")

    return sorted(groups)

def clean_text(text):
    """
    Limpia y normaliza el texto de los issues.
    
    Args:
        text: Texto crudo a limpiar
        
    Returns:
        str: Texto limpio y normalizado
    """
    if not text or not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r"http\S+", "", text)        # URLs
    text = re.sub(r"`.*?`", "", text)          # código inline
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)  # bloques de código
    text = re.sub(r"[^a-z\s]", " ", text)      # símbolos
    text = re.sub(r"\s+", " ", text).strip()   # espacios múltiples
    return text


def build_corpus():
    """
    Construye el corpus procesado desde el dataset crudo.
    
    Proceso:
    1. Lee issues_raw.json
    2. Combina título + cuerpo de cada issue
    3. Limpia el texto
    4. Extrae labels
    5. (NUEVO) Filtra labels raras por frecuencia global
    6. Guarda en corpus.csv
    """
    print("\n" + "="*80)
    print("🔄 PREPROCESANDO DATASET: JSON → CSV")
    print("="*80 + "\n")
    
    # Verificar archivo de entrada
    print(f"[INFO] Buscando archivo de entrada: {INPUT_FILE}")
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"❌ Archivo de entrada no encontrado: {INPUT_FILE}\n"
            f"   Ejecuta primero: python collection/build_raw_dataset.py"
        )
    
    print(f"[OK] Archivo encontrado\n")
    
    # Leer datos crudos
    print("[PASO 1/4] Leyendo datos crudos desde JSON...")
    print("-" * 80)
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            issues = json.load(f)
        print(f"[OK] {len(issues)} issues cargados desde JSON")
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Error al parsear JSON: {str(e)}")
    except Exception as e:
        raise ValueError(f"❌ Error al leer archivo: {str(e)}")
    
    # Crear directorio de salida
    output_dir = os.path.dirname(OUTPUT_FILE)
    os.makedirs(output_dir, exist_ok=True)
    print(f"[OK] Directorio de salida listo: {output_dir}\n")
    
    # Procesar issues (primera pasada)
    print("[PASO 2/4] Procesando issues (limpieza de texto y extracción de labels)...")
    print("-" * 80)
    
    processed_issues = []
    issues_without_text = 0
    issues_without_labels = 0
    total_labels = 0
    
    for idx, issue in enumerate(issues, 1):
        # Extraer y combinar texto
        title = issue.get("title", "") or ""
        body = issue.get("body", "") or ""
        text = f"{title} {body}".strip()
        
        # Limpiar texto
        cleaned_text = clean_text(text)
        
        if not cleaned_text or len(cleaned_text.strip()) == 0:
            issues_without_text += 1
            if idx <= 5:  # Mostrar solo los primeros 5 como ejemplo
                print(f"  ⚠ Issue #{issue.get('issue_id', '?')}: sin texto válido después de limpieza")
            continue
        
        # Extraer labels
        labels = issue.get("labels", [])
        if not labels:
            labels = []
            issues_without_labels += 1
        
        total_labels += len(labels)

        raw_labels = [str(label) for label in labels if label]
        grouped_labels = map_labels_to_groups(raw_labels)

        processed_issues.append({
            "issue_id": issue.get("issue_id", idx),
            "text": cleaned_text,
            "labels_list": grouped_labels
        })

        
        # Mostrar progreso cada 10 issues
        if idx % 10 == 0:
            print(f"  Procesados {idx}/{len(issues)} issues...")
    
    print(f"\n[OK] Procesamiento completado:")
    print(f"   - Issues procesados exitosamente: {len(processed_issues)}")
    print(f"   - Issues sin texto válido: {issues_without_text}")
    print(f"   - Issues sin labels: {issues_without_labels}")
    print(f"   - Total de labels encontrados (antes de filtrar): {total_labels}")
    
    if len(processed_issues) == 0:
        raise ValueError("❌ No se pudo procesar ningún issue. Verifica los datos de entrada.")
    
    # ============================================
    # ✅ NUEVO: FILTRAR LABELS RARAS POR FRECUENCIA
    # ============================================
    print(f"\n[INFO] Filtrando etiquetas raras (frecuencia mínima = {MIN_LABEL_FREQ})...")
    all_labels = []
    for item in processed_issues:
        all_labels.extend(item["labels_list"])

    label_counter = Counter(all_labels)
    valid_labels = {lbl for lbl, c in label_counter.items() if c >= MIN_LABEL_FREQ}

    print(f"[INFO] Labels antes del filtrado: {len(label_counter)}")
    print(f"[INFO] Labels después del filtrado: {len(valid_labels)}")

    # Aplicar filtro a cada issue
    filtered_issues = []
    filtered_total_labels = 0
    issues_left_without_labels = 0

    for item in processed_issues:
        filtered_labels = [lbl for lbl in item["labels_list"] if lbl in valid_labels]
        if not filtered_labels:
            issues_left_without_labels += 1

        filtered_total_labels += len(filtered_labels)

        filtered_issues.append({
            "issue_id": item["issue_id"],
            "text": item["text"],
            "labels": ";".join(filtered_labels)  # ya en formato final
        })

    print(f"[OK] Total de labels después del filtrado: {filtered_total_labels}")
    print(f"[INFO] Issues que quedaron sin labels tras filtrado: {issues_left_without_labels}/{len(filtered_issues)}")

    # Guardar corpus
    print(f"\n[PASO 3/4] Guardando corpus en CSV...")
    print("-" * 80)
    
    try:
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["issue_id", "text", "labels"])
            
            for issue in filtered_issues:
                writer.writerow([
                    issue["issue_id"],
                    issue["text"],
                    issue["labels"]
                ])
        
        print(f"[OK] Corpus guardado exitosamente en: {OUTPUT_FILE}")
    except Exception as e:
        raise ValueError(f"❌ Error al guardar corpus: {str(e)}")
    
    # Estadísticas finales
    print(f"\n[PASO 4/4] Estadísticas del corpus generado:")
    print("-" * 80)
    
    # Calcular estadísticas de texto
    text_lengths = [len(issue["text"]) for issue in filtered_issues]
    avg_text_length = sum(text_lengths) / len(text_lengths) if text_lengths else 0
    
    # Calcular estadísticas de labels
    label_counts = [len(issue["labels"].split(";")) if issue["labels"] else 0 
                    for issue in filtered_issues]
    avg_labels = sum(label_counts) / len(label_counts) if label_counts else 0
    
    # Contar labels únicos (después del filtrado)
    all_labels_after = []
    for issue in filtered_issues:
        if issue["labels"]:
            all_labels_after.extend(issue["labels"].split(";"))
    unique_labels_after = len(set(all_labels_after))
    
    print(f"   - Total de issues en corpus: {len(filtered_issues)}")
    print(f"   - Longitud promedio de texto: {avg_text_length:.0f} caracteres")
    print(f"   - Promedio de labels por issue: {avg_labels:.2f}")
    print(f"   - Labels únicos encontrados (después de filtrar): {unique_labels_after}")
    
    # Mostrar algunos labels más frecuentes
    if all_labels_after:
        label_freq = Counter(all_labels_after)
        top_labels = label_freq.most_common(10)
        print(f"\n   Top 10 labels más frecuentes (después de filtrar):")
        for label, count in top_labels:
            print(f"     - {label}: {count} veces")
    
    print("\n" + "="*80)
    print("✅ PREPROCESAMIENTO COMPLETADO EXITOSAMENTE")
    print("="*80)
    print(f"\n📁 Archivo generado: {OUTPUT_FILE}")
    print(f"📊 Listo para usar en: python experiments/run_tfidf_rf_baseline.py\n")


if __name__ == "__main__":
    build_corpus()
