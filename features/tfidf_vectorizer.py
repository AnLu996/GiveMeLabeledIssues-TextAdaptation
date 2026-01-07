"""
TF-IDF Vectorizer Module
========================

Transforma texto limpio en vectores numéricos TF-IDF para entrenamiento de modelos ML.
"""

import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFVectorizer:
    """
    Wrapper para sklearn TfidfVectorizer con funcionalidades adicionales.
    
    Permite guardar y cargar el vectorizador entrenado para reutilización.
    """
    
    def __init__(self, max_features=5000, min_df=2, max_df=0.95, ngram_range=(1, 2)):
        """
        Inicializa el vectorizador TF-IDF.
        
        Args:
            max_features: Número máximo de características a considerar
            min_df: Frecuencia mínima de documentos para una palabra
            max_df: Frecuencia máxima de documentos para una palabra
            ngram_range: Rango de n-gramas (tupla de min, max)
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            ngram_range=ngram_range,
            lowercase=True,
            stop_words='english'
        )
        self.is_fitted = False
    
    def fit(self, texts):
        """
        Entrena el vectorizador con los textos proporcionados.
        
        Args:
            texts: Lista o Serie de textos a procesar
            
        Returns:
            self: Para permitir method chaining
        """
        self.vectorizer.fit(texts)
        self.is_fitted = True
        return self
    
    def transform(self, texts):
        """
        Transforma textos a vectores TF-IDF.
        
        Args:
            texts: Lista o Serie de textos a transformar
            
        Returns:
            scipy.sparse.csr_matrix: Matriz sparse con los vectores TF-IDF
        """
        if not self.is_fitted:
            raise ValueError("El vectorizador debe ser entrenado primero con fit()")
        return self.vectorizer.transform(texts)
    
    def fit_transform(self, texts):
        """
        Entrena y transforma los textos en un solo paso.
        
        Args:
            texts: Lista o Serie de textos a procesar
            
        Returns:
            scipy.sparse.csr_matrix: Matriz sparse con los vectores TF-IDF
        """
        result = self.vectorizer.fit_transform(texts)
        self.is_fitted = True
        return result
    
    def get_feature_names(self):
        """
        Obtiene los nombres de las características (palabras/n-gramas).
        
        Returns:
            list: Lista de nombres de características
        """
        if not self.is_fitted:
            raise ValueError("El vectorizador debe ser entrenado primero con fit()")
        return self.vectorizer.get_feature_names_out().tolist()
    
    def save(self, filepath):
        """
        Guarda el vectorizador entrenado en disco.
        
        Args:
            filepath: Ruta donde guardar el modelo
        """
        if not self.is_fitted:
            raise ValueError("El vectorizador debe ser entrenado primero antes de guardar")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"[OK] Vectorizador guardado en {filepath}")
    
    def load(self, filepath):
        """
        Carga un vectorizador previamente guardado.
        
        Args:
            filepath: Ruta del archivo del modelo guardado
            
        Returns:
            self: Para permitir method chaining
        """
        with open(filepath, 'rb') as f:
            self.vectorizer = pickle.load(f)
        self.is_fitted = True
        print(f"[OK] Vectorizador cargado desde {filepath}")
        return self
