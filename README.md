# GiveMeLabeledIssues - Text Adaptation & API

Este proyecto consta de dos componentes principales:
1.  **API Backend (`baseline_api/`)**: Una API REST en Django que sirve las predicciones (implementación original).
2.  **Text Adaptation Pipeline (Raíz)**: Scripts de experimentación y mejora del modelo usando NLP (el trabajo actual).

---

## 🏗️ 1. Cómo ejecutar el Backend (API)

Esta es la aplicación web (Django) que sirve el modelo.

### Prerrequisitos
- Python 3.8+
- Virtualenv (recomendado)

### Instalación
1.  Navegar al directorio del backend:
    ```bash
    cd baseline_api
    ```
2.  Crear entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # o
    venv\Scripts\activate     # Windows
    ```
3.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

### Ejecutar Servidor
```bash
python manage.py runserver
```
El servidor correrá en `http://127.0.0.1:8000/`.

---

## 🧪 2. Cómo ejecutar el Text Adaptation Pipeline (Front de Experimentación)

Este pipeline permite recolectar issues, procesarlos y entrenar/evaluar el modelo mejorado (Random Forest + TF-IDF).

### Instalación
Desde la **raíz** del proyecto:
```bash
pip install -r requirements.txt
```

### Flujo Completo
1.  **Preprocesamiento**: Limpia datos y mapea etiquetas (configuración histórica de 4 categorías).
    ```bash
    python preprocessing/build_corpus.py
    ```
    *Genera: `data/processed/corpus.csv`*

2.  **Entrenamiento y Evaluación**: Entrena el modelo y muestra métricas.
    ```bash
    python experiments/run_tfidf_rf_baseline.py
    ```
    *Resultado esperado: F1 Macro ~0.56*

---

## 🤖 ¿Ayudaría BERT a mejorar las métricas?

**Respuesta Corta**: Probablemente **NO** de manera significativa (y podría ser contraproducente con los datos actuales).

**Análisis Detallado**:
1.  **Escasez de Datos (Small Data)**: Tenemos solo ~300 issues. BERT requiere miles de ejemplos para un "fine-tuning" efectivo. Con tan pocos datos, BERT tiende a **sobreajustarse** (memorizar en lugar de aprender).
2.  **Naturaleza del Problema**: Las etiquetas (`PRIORITY`, `COMPONENT`, `DEVELOPMENT`) son muy dependientes de **palabras clave** (e.g., "fix", "ui", "test"). TF-IDF captura estas palabras clave de manera excelente y eficiente. BERT busca contexto semántico profundo ("entender el significado"), lo cual es excesivo y ruidoso para una clasificación tan técnica y basada en keywords.
3.  **Costo-Beneficio**: Implementar BERT aumentaría el tiempo de entrenamiento de segundos a horas (sin GPU) y el tamaño del modelo de MB a GB, para una ganancia de rendimiento marginal (o negativa) frente al ~0.56 robusto de TF-IDF.

**Recomendación**: Mantener **TF-IDF + Random Forest** como la solución óptima para este volumen de datos. Si el dataset crece a >5,000 issues, entonces sí valdría la pena re-evaluar BERT.
