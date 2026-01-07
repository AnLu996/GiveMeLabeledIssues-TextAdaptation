"""
Evaluation Module
=================

Módulo para evaluación de modelos de clasificación multi-etiqueta.
"""

from .metrics import (
    evaluate_multilabel,
    evaluate_per_label,
    print_classification_report,
    evaluate
)

__all__ = [
    'evaluate_multilabel',
    'evaluate_per_label',
    'print_classification_report',
    'evaluate'
]
