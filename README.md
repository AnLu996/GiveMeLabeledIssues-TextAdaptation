# GiveMeLabeledIssues – Text Adaptation with Skill-Based Recommendation

Este proyecto presenta una **adaptación del sistema GiveMeLabeledIssues** orientada a la recomendación de *issues* en proyectos de software de código abierto (OSS), basada **exclusivamente en información textual** disponible en los repositorios, sin depender del análisis del código fuente ni de la trazabilidad explícita entre *issues*, *pull requests* y APIs.

La propuesta busca ampliar la aplicabilidad del enfoque original mediante un **pipeline de procesamiento de lenguaje natural (NLP) y aprendizaje automático**, que permite:

* clasificar *issues* abiertos,
* inferir habilidades técnicas requeridas,
* y generar **recomendaciones personalizadas de issues** según el perfil de habilidades de un desarrollador.

---

## 📌 Características principales

* Construcción de un **corpus textual** a partir de:

  * títulos y descripciones de *issues*,
  * comentarios de *issues* (cuando están disponibles),
  * mensajes de *commits* asociados (cuando están disponibles).
* Preprocesamiento del texto (limpieza, normalización).
* Clasificación multi-etiqueta de *issues* usando:

  * **TF-IDF + Random Forest** (baseline).
  * **Embeddings BERT + One-vs-Rest Logistic Regression** (modelo contextual).
* Inferencia de **habilidades técnicas (skills)** desde texto.
* Generación de **recomendaciones personalizadas de issues** según el perfil de habilidades de un desarrollador.
* Evaluación experimental con métricas estándar (precision, recall, F1-score, etc.).

---

## 🧩 Pipeline del sistema

El pipeline completo implementado es el siguiente:

1. **Recolección de datos textuales**

   * Issues (title + body)
   * Comentarios y mensajes de commits (si existen)
2. **Preprocesamiento del texto**
3. **Construcción del corpus**
4. **Entrenamiento y evaluación de modelos**

   * TF-IDF + Random Forest
   * BERT (embeddings) + clasificador
5. **Clasificación de issues abiertos**
6. **Inferencia de habilidades técnicas**
7. **Recomendación personalizada de issues**
8. **Exportación de resultados**

---

## 📁 Estructura del repositorio

```
GiveMeLabeledIssues-TextAdaptation/
├── data/
│   ├── raw/
│   │   └── issues_raw.json
│   └── processed/
│       └── corpus.csv
├── preprocessing/
│   └── build_corpus.py
├── experiments/
│   ├── run_tfidf_rf_baseline.py
│   ├── run_bert_embeddings_baseline.py
│   ├── run_recommender_demo.py
│   ├── run_recommender_with_predictions.py
│   └── output/
│       ├── predicciones_test.json
│       └── recomendaciones.json
├── recommender/
│   ├── skills.json
│   ├── skill_extractor.py
│   └── recommend_issues.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos

* Python 3.9+
* Crear y activar un entorno virtual (recomendado)
* Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Cómo ejecutar el pipeline (paso a paso)

### 1️⃣ Construcción del corpus textual

Genera `data/processed/corpus.csv` a partir de los issues crudos.

```bash
python preprocessing/build_corpus.py
```

En consola se mostrará información sobre:

* número de issues procesados,
* issues sin texto,
* distribución y filtrado de etiquetas.

---

### 2️⃣ Clasificación baseline (TF-IDF + Random Forest)

Entrena el modelo base, evalúa métricas y exporta predicciones.

```bash
python experiments/run_tfidf_rf_baseline.py
```

Resultados:

* Métricas de clasificación (macro/micro F1, precision, recall, etc.).
* Archivo generado:

  ```
  experiments/output/predicciones_test.json
  ```

---

### 3️⃣ Recomendación personalizada de issues

Utiliza las etiquetas predichas + habilidades del desarrollador para recomendar issues.

```bash
python experiments/run_recommender_with_predictions.py
```

Resultados:

* Top-k issues recomendados mostrados en consola.
* Archivo generado:

  ```
  experiments/output/recomendaciones.json
  ```

---

### 4️⃣ Modelo contextual basado en BERT

Ejecuta el experimento con embeddings BERT y compara contra el baseline.

```bash
python experiments/run_bert_embeddings_baseline.py
```

Resultados:

* Métricas comparables con el baseline TF-IDF.
* Evaluación del impacto de representaciones semánticas contextuales.

---

## 🧪 Evaluación

Se utilizan métricas estándar de clasificación multi-etiqueta:

* Precision
* Recall
* F1-score (micro y macro)
* Hamming loss
* Jaccard score

Los resultados permiten comparar:

* TF-IDF + Random Forest
* BERT embeddings + clasificador lineal

---

## 👤 Recomendación basada en habilidades

El sistema infiere habilidades técnicas desde el texto de cada issue (por ejemplo: `python`, `ml`, `data`, `git`, `testing`) y recomienda issues según el perfil del desarrollador, definido como un conjunto ponderado de habilidades.

Ejemplo de perfil:

```python
developer_skills = {
  "python": 1.0,
  "data": 0.8,
  "ml": 0.6,
  "git": 0.4
}
```

---

## ⚠️ Limitaciones conocidas

* Algunas etiquetas (por ejemplo `DEVELOPMENT`) presentan baja frecuencia, lo que afecta su desempeño.
* En el dataset utilizado predominan títulos y descripciones de issues; comentarios y commits se integran cuando están disponibles.
* El modelo BERT se usa como extractor de embeddings (no fine-tuning completo).

---

## 📚 Relación con el trabajo original

Este proyecto adapta la filosofía de *GiveMeLabeledIssues*, eliminando la dependencia del análisis del código fuente y priorizando información textual más accesible y generalizable, manteniendo el enfoque de **recomendación basada en habilidades**.

---

## 🏁 Conclusión

La adaptación implementada demuestra que es posible construir un sistema de recomendación de issues basado en habilidades utilizando únicamente fuentes textuales, logrando resultados competitivos y mayor flexibilidad para proyectos OSS con información limitada del código.


## 👁️ Visualizador de Corpus (`index.html`)

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


