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

## 👁️ 3. Visualizador de Corpus (`index.html`)

Si deseas explorar los datos procesados (`corpus.csv`) usando la interfaz `index.html`:

1.  **Ejecutar el servidor ligero (Flask)**:
    ```bash
    python baseline_api/app.py
    ```
    *Esto levanta un servidor en `http://127.0.0.1:5000` que lee el `corpus.csv`.*

2.  **Abrir `index.html`**:
    Simplemente abre el archivo `index.html` (ubicado en la raíz) con tu navegador web (doble clic). 
    La interfaz se conectará al servidor local para mostrar filtrar issues por etiqueta o texto.

---


