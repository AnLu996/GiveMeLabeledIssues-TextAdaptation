"""
Random Forest Multi-Label Classifier
=====================================

Clasificador multi-etiqueta usando Random Forest para etiquetado de issues.
"""

import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier


class RandomForestMultiLabel:
    """
    Clasificador Random Forest para problemas multi-etiqueta.
    
    Utiliza MultiOutputClassifier para manejar múltiples etiquetas por instancia.
    """
    
    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2, 
                 min_samples_leaf=1, random_state=42, n_jobs=-1):
        """
        Inicializa el clasificador Random Forest multi-etiqueta.
        
        Args:
            n_estimators: Número de árboles en el bosque
            max_depth: Profundidad máxima de los árboles (None = sin límite)
            min_samples_split: Mínimo de muestras para dividir un nodo
            min_samples_leaf: Mínimo de muestras en una hoja
            random_state: Semilla para reproducibilidad
            n_jobs: Número de trabajos paralelos (-1 = todos los cores)
        """
        base_estimator = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
            n_jobs=n_jobs,
            verbose=0
        )
        
        self.model = MultiOutputClassifier(base_estimator)
        self.is_fitted = False
    
    def fit(self, X, y):
        """
        Entrena el modelo con los datos proporcionados.
        
        Args:
            X: Matriz de características (vectores TF-IDF)
            y: Matriz binaria de etiquetas (n_samples, n_labels)
            
        Returns:
            self: Para permitir method chaining
        """
        print(f"[INFO] Entrenando Random Forest con {X.shape[0]} muestras y {y.shape[1]} etiquetas...")
        self.model.fit(X, y)
        self.is_fitted = True
        print("[OK] Modelo entrenado exitosamente")
        return self
    
    def predict(self, X):
        """
        Predice etiquetas para nuevas instancias.
        
        Args:
            X: Matriz de características a predecir
            
        Returns:
            numpy.ndarray: Matriz binaria de predicciones (n_samples, n_labels)
        """
        if not self.is_fitted:
            raise ValueError("El modelo debe ser entrenado primero con fit()")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Predice probabilidades para cada etiqueta.
        
        Args:
            X: Matriz de características a predecir
            
        Returns:
            numpy.ndarray: Matriz de probabilidades (n_samples, n_labels)
        """
        if not self.is_fitted:
            raise ValueError("El modelo debe ser entrenado primero con fit()")
        return self.model.predict_proba(X)
    
    def get_feature_importances(self):
        """
        Obtiene la importancia de características promedio de todos los clasificadores.
        
        Returns:
            numpy.ndarray: Importancia promedio de características por etiqueta
        """
        if not self.is_fitted:
            raise ValueError("El modelo debe ser entrenado primero con fit()")
        
        importances = []
        for estimator in self.model.estimators_:
            importances.append(estimator.feature_importances_)
        
        return np.mean(importances, axis=0)
    
    def save(self, filepath):
        """
        Guarda el modelo entrenado en disco.
        
        Args:
            filepath: Ruta donde guardar el modelo
        """
        if not self.is_fitted:
            raise ValueError("El modelo debe ser entrenado primero antes de guardar")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"[OK] Modelo guardado en {filepath}")
    
    def load(self, filepath):
        """
        Carga un modelo previamente guardado.
        
        Args:
            filepath: Ruta del archivo del modelo guardado
            
        Returns:
            self: Para permitir method chaining
        """
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        self.is_fitted = True
        print(f"[OK] Modelo cargado desde {filepath}")
        return self
