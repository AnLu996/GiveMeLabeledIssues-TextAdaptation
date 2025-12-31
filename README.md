# GiveMeLabeledIssues – Adaptación Basada en Texto

Este proyecto se basa en el sistema original **GiveMeLabeledIssues**, cuyo objetivo
es recomendar issues de proyectos open source según dominios de conocimiento
(UI, DB, etc.).  
A partir de este sistema base, se propone una **adaptación orientada a gestión de
proyectos**, específicamente a **backlog grooming y priorización**, utilizando
únicamente información textual.

El repositorio está organizado para separar claramente:
- la **implementación base del paper original**, y
- la **adaptación propuesta basada en texto**.

---

## Estructura del Repositorio

```

baseline_api/        # Sistema base del paper original (API GiveMeLabeledIssues)
collection/          # Recolección de issues desde GitHub
preprocessing/       # Limpieza y normalización de texto
features/            # Extracción de características (TF-IDF, BERT)
models/              # Modelos de ML (Random Forest, BERT)
experiments/         # Ejecución del pipeline completo
evaluation/          # Métricas de evaluación
data/                # Datos crudos y procesados
notebooks/           # Análisis y experimentos

````

---

## Parte 1: Sistema Base (Paper Original)

La carpeta `baseline_api/` contiene la implementación original del sistema
**GiveMeLabeledIssues**, desarrollada con Django REST Framework.  
Esta versión **funciona de forma independiente** y ya incluye una **base de datos
de ejemplo**, lo que permite probar el sistema sin necesidad de entrenar modelos.

---

### Requisitos del Sistema Base
- Python 3.9 – 3.11
- pip

---

### Instalación del Sistema Base

#### Linux / macOS

```bash
cd baseline_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
````

#### Windows (PowerShell)

```powershell
cd baseline_api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

### Prueba del Sistema Base

Una vez levantado el servidor, abrir en el navegador:

```text
http://127.0.0.1:8000/
```

Para probar el endpoint principal de recomendación:

```bash
curl -s "http://127.0.0.1:8000/Query/JabRef,jabref/UI" | head -c 200
```

Comportamiento esperado:

* Respuesta HTTP 200
* Salida en formato JSON con una lista de issues recomendados

Esto confirma que:

* el backend está funcionando correctamente,
* la base de datos está conectada,
* el pipeline de recomendación del paper original es ejecutable.

---

## Parte 2: Adaptación Basada en Texto (Propuesta del Proyecto)

El resto del repositorio corresponde a la **adaptación propuesta** del sistema.
A diferencia del enfoque original, esta versión **no depende del análisis de
código fuente**, sino únicamente de **información textual**, como:

* título de los issues
* descripción de los issues
* (opcionalmente) mensajes de commits

El objetivo es apoyar **backlog grooming y priorización de issues** mediante
técnicas de Procesamiento de Lenguaje Natural (NLP).

---

### Flujo General de la Adaptación

1. **Recolección de Issues** desde GitHub
2. **Preprocesamiento de Texto** (limpieza y normalización)
3. **Extracción de Características**

   * TF-IDF
   * Embeddings con BERT
4. **Entrenamiento de Modelos**

   * Random Forest
   * Clasificador basado en BERT
5. **Evaluación** con métricas como Precision, Recall, F1-score y Hamming Loss

---

### Ejecución del Pipeline de la Adaptación

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el pipeline completo:

```bash
python experiments/run_pipeline.py
```

Los datos intermedios y finales se almacenan en:

* `data/raw/`
* `data/processed/`

Las métricas de evaluación se calculan en:

```
evaluation/metrics.py
```

---

## Notas Importantes

* El sistema base y la adaptación se mantienen separados para facilitar la
  comparación y evaluación.
* La inclusión del sistema base garantiza la **reproducibilidad del paper
  original**.
* La adaptación está orientada a **gestión de proyectos de software**, en
  particular a tareas de **priorización del backlog**.

---

## Resumen

* `baseline_api/` → implementación original del paper (ejecutable)
* resto del repositorio → adaptación basada en texto y experimentos

Esta organización permite validar el sistema original antes de introducir las
modificaciones propuestas.

```

---

Si quieres, en el siguiente mensaje puedo:
- ayudarte a escribir **el texto del Pull Request**,
- revisar que el README esté alineado con el informe final,
- o ayudarte a resumir esto en **2–3 diapositivas para exposición**.
```
