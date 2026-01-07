"""
Métricas de Evaluación para Clasificación Multi-Etiqueta
=========================================================

Funciones para evaluar modelos de clasificación multi-etiqueta.
"""

import numpy as np
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    hamming_loss, jaccard_score, classification_report,
    multilabel_confusion_matrix
)


def evaluate_multilabel(y_true, y_pred, average='macro'):
    """
    Calcula métricas básicas para clasificación multi-etiqueta.
    
    Args:
        y_true: Matriz binaria de etiquetas verdaderas (n_samples, n_labels)
        y_pred: Matriz binaria de predicciones (n_samples, n_labels)
        average: Tipo de promedio ('macro', 'micro', 'weighted', 'samples')
    
    Returns:
        dict: Diccionario con las métricas calculadas
    """
    metrics = {
        "precision": precision_score(y_true, y_pred, average=average, zero_division=0),
        "recall": recall_score(y_true, y_pred, average=average, zero_division=0),
        "f1": f1_score(y_true, y_pred, average=average, zero_division=0),
        "hamming_loss": hamming_loss(y_true, y_pred),
        "jaccard_score": jaccard_score(y_true, y_pred, average=average, zero_division=0)
    }
    
    return metrics


def evaluate_per_label(y_true, y_pred, label_names=None):
    """
    Calcula métricas por etiqueta individual.
    
    Args:
        y_true: Matriz binaria de etiquetas verdaderas (n_samples, n_labels)
        y_pred: Matriz binaria de predicciones (n_samples, n_labels)
        label_names: Lista de nombres de etiquetas (opcional)
    
    Returns:
        dict: Diccionario con métricas por etiqueta
    """
    n_labels = y_true.shape[1]
    
    if label_names is None:
        label_names = [f"Label_{i}" for i in range(n_labels)]
    
    per_label_metrics = {}
    
    for i, label_name in enumerate(label_names):
        per_label_metrics[label_name] = {
            "precision": precision_score(y_true[:, i], y_pred[:, i], zero_division=0),
            "recall": recall_score(y_true[:, i], y_pred[:, i], zero_division=0),
            "f1": f1_score(y_true[:, i], y_pred[:, i], zero_division=0)
        }
    
    return per_label_metrics


def print_classification_report(y_true, y_pred, label_names=None):
    """
    Imprime un reporte completo de clasificación multi-etiqueta.
    
    Args:
        y_true: Matriz binaria de etiquetas verdaderas (n_samples, n_labels)
        y_pred: Matriz binaria de predicciones (n_samples, n_labels)
        label_names: Lista de nombres de etiquetas (opcional)
    """
    if label_names is None:
        label_names = [f"Label_{i}" for i in range(y_true.shape[1])]
    
    print("\n" + "="*80)
    print("REPORTE DE CLASIFICACIÓN MULTI-ETIQUETA")
    print("="*80)
    print(classification_report(y_true, y_pred, target_names=label_names, zero_division=0))
    print("="*80 + "\n")


def evaluate(y_true, y_pred):
    """
    Función de compatibilidad con código anterior (clasificación binaria simple).
    
    Args:
        y_true: Etiquetas verdaderas
        y_pred: Predicciones
    
    Returns:
        dict: Diccionario con métricas básicas
    """
    return {
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0)
    }
