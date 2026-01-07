"""
Pipeline Baseline: TF-IDF + Random Forest
==========================================

Pipeline completo para el baseline del paper que incluye:
- Lectura del corpus
- Conversión de texto a TF-IDF
- Conversión de labels a formato multi-etiqueta
- Entrenamiento de Random Forest
- Evaluación con métricas básicas
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer

# Agregar el directorio raíz al path para imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from features.tfidf_vectorizer import TFIDFVectorizer
from models.random_forest import RandomForestMultiLabel
from evaluation.metrics import (
    evaluate_multilabel, 
    evaluate_per_label, 
    print_classification_report
)


def load_corpus(corpus_path):
    """
    Carga el corpus desde un archivo CSV.
    
    Args:
        corpus_path: Ruta al archivo corpus.csv
        
    Returns:
        pandas.DataFrame: DataFrame con columnas issue_id, text, labels
    """
    print(f"[INFO] Cargando corpus desde {corpus_path}...")
    
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Archivo no encontrado: {corpus_path}")
    
    df = pd.read_csv(corpus_path)
    print(f"[OK] Corpus cargado: {len(df)} issues")
    print(f"[INFO] Columnas disponibles: {list(df.columns)}")
    
    return df


def prepare_labels(labels_series):
    """
    Convierte las etiquetas de string separado por ';' a formato multi-etiqueta.
    
    Args:
        labels_series: Serie de pandas con strings de labels separados por ';'
        
    Returns:
        tuple: (y_binary, label_names, mlb)
            - y_binary: Matriz binaria de etiquetas (n_samples, n_labels)
            - label_names: Lista de nombres de etiquetas únicas
            - mlb: MultiLabelBinarizer entrenado
    """
    print("[INFO] Preparando etiquetas multi-etiqueta...")
    
    # Convertir strings a listas de labels
    labels_list = labels_series.apply(
        lambda x: [label.strip() for label in str(x).split(';') if label.strip()]
    )
    
    # Verificar que hay etiquetas
    total_labels = sum(len(labels) for labels in labels_list)
    issues_with_labels = sum(1 for labels in labels_list if len(labels) > 0)
    
    print(f"[DEBUG] Issues con etiquetas: {issues_with_labels}/{len(labels_list)}")
    print(f"[DEBUG] Total de etiquetas (antes de binarizar): {total_labels}")
    
    if total_labels == 0:
        raise ValueError("❌ No se encontraron etiquetas en el dataset. Verifica el formato de labels.")
    
    # Crear y entrenar MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    y_binary = mlb.fit_transform(labels_list)
    label_names = mlb.classes_.tolist()
    
    print(f"[OK] {len(label_names)} etiquetas únicas encontradas")
    print(f"[INFO] Distribución de etiquetas por muestra:")
    print(f"  - Promedio de etiquetas por issue: {y_binary.sum(axis=1).mean():.2f}")
    print(f"  - Mínimo: {y_binary.sum(axis=1).min()}, Máximo: {y_binary.sum(axis=1).max()}")
    print(f"  - Total de etiquetas en matriz binaria: {y_binary.sum()}")
    
    # Verificar que la matriz binaria tiene datos
    if y_binary.sum() == 0:
        raise ValueError("❌ La matriz binaria de etiquetas está vacía. Verifica el procesamiento.")
    
    # Mostrar las etiquetas más frecuentes
    label_counts = y_binary.sum(axis=0)
    top_labels = sorted(zip(label_names, label_counts), key=lambda x: x[1], reverse=True)[:10]
    print(f"\n[INFO] Top 10 etiquetas más frecuentes:")
    for label, count in top_labels:
        if count > 0:
            print(f"  - {label}: {count} ({count/len(labels_list)*100:.1f}%)")
    
    return y_binary, label_names, mlb


def main():
    """
    Función principal que ejecuta el pipeline completo.
    """
    print("\n" + "="*80)
    print("🚀 PIPELINE BASELINE: TF-IDF + RANDOM FOREST")
    print("="*80 + "\n")
    
    # ============================================
    # 1. CONFIGURACIÓN DE RUTAS
    # ============================================
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CORPUS_PATH = os.path.join(BASE_DIR, "data", "processed", "corpus.csv")
    
    # ============================================
    # 2. CARGAR CORPUS
    # ============================================
    df = load_corpus(CORPUS_PATH)
    
    # Verificar que tenemos las columnas necesarias
    required_columns = ['issue_id', 'text', 'labels']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Columnas faltantes en el corpus: {missing_columns}")
    
    # Advertencia sobre tamaño del dataset
    if len(df) < 50:
        print(f"\n⚠️  ADVERTENCIA: Dataset pequeño ({len(df)} issues)")
        print("   Para obtener mejores resultados, se recomienda al menos 50-100 issues.")
        print("   Puedes recolectar más datos ejecutando:")
        print("   python collection/build_raw_dataset.py")
        #print("   (Ajusta MAX_ISSUES en github_issues_collector.py para obtener más)\n")
    
    # ============================================
    # 3. PREPARAR DATOS
    # ============================================
    # Separar características y etiquetas
    X_text = df['text'].fillna('')  # Asegurar que no haya NaN
    y_labels = df['labels'].fillna('')  # Asegurar que no haya NaN
    
    # Convertir labels a formato multi-etiqueta
    y_binary, label_names, mlb = prepare_labels(y_labels)
    
    # ============================================
    # 4. DIVIDIR EN TRAIN/TEST
    # ============================================
    print("\n[INFO] Dividiendo datos en conjunto de entrenamiento y prueba...")
    
    # Ajustar test_size según cantidad de datos
    n_samples = len(X_text)
    if n_samples < 20:
        test_size = max(0.1, 2 / n_samples)  # Mínimo 2 muestras en test
        print(f"[ADVERTENCIA] Dataset pequeño ({n_samples} muestras). Ajustando test_size a {test_size:.2f}")
    else:
        test_size = 0.2
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_text,
        y_binary,
        test_size=test_size,
        random_state=42,
        stratify=None  # No podemos estratificar en multi-etiqueta directamente
    )
    
    print(f"[OK] Conjunto de entrenamiento: {len(X_train)} muestras")
    print(f"[OK] Conjunto de prueba: {len(X_test)} muestras")
    
    # Validaciones críticas
    if len(X_train) == 0:
        raise ValueError("❌ El conjunto de entrenamiento está vacío. Necesitas más datos.")
    if len(X_test) == 0:
        raise ValueError("❌ El conjunto de prueba está vacío. Necesitas más datos.")
    
    # Verificar que hay etiquetas en train y test
    train_labels_sum = y_train.sum()
    test_labels_sum = y_test.sum()
    print(f"[INFO] Etiquetas en entrenamiento: {train_labels_sum} total")
    print(f"[INFO] Etiquetas en prueba: {test_labels_sum} total")
    
    if train_labels_sum == 0:
        raise ValueError("❌ No hay etiquetas en el conjunto de entrenamiento.")
    if test_labels_sum == 0:
        print("[ADVERTENCIA] No hay etiquetas en el conjunto de prueba. Las métricas pueden ser 0.")
    
    # ============================================
    # 5. VECTORIZACIÓN TF-IDF
    # ============================================
    print("\n[INFO] Aplicando vectorización TF-IDF...")
    
    # Ajustar parámetros según tamaño del dataset
    if n_samples < 20:
        min_df = 1  # Con pocos datos, aceptar palabras que aparecen solo una vez
        max_features = min(1000, len(X_train) * 10)  # Limitar características
        print(f"[INFO] Dataset pequeño: ajustando min_df={min_df}, max_features={max_features}")
    else:
        min_df = 2
        max_features = 5000
    
    vectorizer = TFIDFVectorizer(
        max_features=max_features,
        min_df=min_df,
        max_df=0.95,
        ngram_range=(1, 2)
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"[OK] Vectores TF-IDF creados")
    print(f"[INFO] Dimensiones train: {X_train_tfidf.shape[0]} muestras x {X_train_tfidf.shape[1]} características")
    print(f"[INFO] Dimensiones test: {X_test_tfidf.shape[0]} muestras x {X_test_tfidf.shape[1]} características")
    
    # Verificar que hay características
    if X_train_tfidf.shape[1] == 0:
        raise ValueError("❌ No se generaron características TF-IDF. Verifica el texto de entrada.")
    
    # ============================================
    # 6. ENTRENAR RANDOM FOREST
    # ============================================
    print("\n[INFO] Entrenando modelo Random Forest...")
    
    # Ajustar parámetros según tamaño del dataset
    if n_samples < 20:
        n_estimators = 50  # Menos árboles para datasets pequeños
        max_depth = 10     # Menor profundidad
        min_samples_split = 2
        min_samples_leaf = 1
        print(f"[INFO] Dataset pequeño: ajustando parámetros del modelo")
    else:
        n_estimators = 100
        max_depth = 50
        min_samples_split = 5
        min_samples_leaf = 2
    
    model = RandomForestMultiLabel(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_tfidf, y_train)
    
    # ============================================
    # 7. PREDICCIONES
    # ============================================
    print("\n[INFO] Realizando predicciones...")
    y_pred = model.predict(X_test_tfidf)
    
    print(f"[OK] Predicciones completadas")
    print(f"[INFO] Shape de predicciones: {y_pred.shape}")
    print(f"[INFO] Total de etiquetas predichas: {y_pred.sum()}")
    print(f"[INFO] Total de etiquetas reales: {y_test.sum()}")
    
    # Verificar que hay predicciones
    if y_pred.sum() == 0:
        print("[ADVERTENCIA] El modelo predijo todas las etiquetas como 0 (sin etiquetas).")
        print("[ADVERTENCIA] Esto puede deberse a:")
        print("  - Dataset muy pequeño para entrenar")
        print("  - Parámetros del modelo muy restrictivos")
        print("  - Desbalance de clases")
    
    # Mostrar algunas predicciones de ejemplo
    print(f"\n[DEBUG] Ejemplo de predicciones (primeras 3 muestras de test):")
    for i in range(min(3, len(X_test))):
        real_labels = [label_names[j] for j in range(len(label_names)) if y_test[i, j] == 1]
        pred_labels = [label_names[j] for j in range(len(label_names)) if y_pred[i, j] == 1]
        print(f"  Muestra {i+1}:")
        print(f"    Real: {real_labels if real_labels else ['ninguna']}")
        print(f"    Pred: {pred_labels if pred_labels else ['ninguna']}")
    
    # ============================================
    # 8. EVALUACIÓN
    # ============================================
    print("\n" + "="*80)
    print("📊 RESULTADOS DE EVALUACIÓN")
    print("="*80)
    
    # Métricas generales
    print("\n[INFO] Métricas generales (promedio macro):")
    metrics_macro = evaluate_multilabel(y_test, y_pred, average='macro')
    for metric_name, metric_value in metrics_macro.items():
        print(f"  - {metric_name}: {metric_value:.4f}")
    
    print("\n[INFO] Métricas generales (promedio micro):")
    metrics_micro = evaluate_multilabel(y_test, y_pred, average='micro')
    for metric_name, metric_value in metrics_micro.items():
        print(f"  - {metric_name}: {metric_value:.4f}")
    
    # Métricas por etiqueta (solo top 10 para no saturar)
    print("\n[INFO] Métricas por etiqueta (Top 10 más frecuentes):")
    per_label_metrics = evaluate_per_label(y_test, y_pred, label_names)
    
    # Ordenar por frecuencia
    label_counts = y_test.sum(axis=0)
    top_indices = np.argsort(label_counts)[::-1][:10]
    
    for idx in top_indices:
        label_name = label_names[idx]
        metrics = per_label_metrics[label_name]
        count = label_counts[idx]
        print(f"\n  {label_name} (frecuencia: {count}):")
        print(f"    - Precision: {metrics['precision']:.4f}")
        print(f"    - Recall: {metrics['recall']:.4f}")
        print(f"    - F1: {metrics['f1']:.4f}")
    
    # Reporte completo de clasificación
    print_classification_report(y_test, y_pred, label_names)
    
    # ============================================
    # 9. RESUMEN FINAL
    # ============================================
    print("\n" + "="*80)
    print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
    print("="*80)
    print(f"\nResumen:")
    print(f"  - Total de issues procesados: {len(df)}")
    print(f"  - Issues de entrenamiento: {len(X_train)}")
    print(f"  - Issues de prueba: {len(X_test)}")
    print(f"  - Total de etiquetas únicas: {len(label_names)}")
    print(f"  - Características TF-IDF: {X_train_tfidf.shape[1]}")
    print(f"  - F1-Score (macro): {metrics_macro['f1']:.4f}")
    print(f"  - F1-Score (micro): {metrics_micro['f1']:.4f}")
    print(f"  - Hamming Loss: {metrics_macro['hamming_loss']:.4f}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
