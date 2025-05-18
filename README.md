# Proyecto: Detección de Cáncer en la Piel por Clasificación de Imágenes

Este proyecto tiene como objetivo detectar cáncer en la piel a partir de imágenes de lesiones cutáneas utilizando técnicas de clasificación de imágenes. Para ello, se utiliza un dataset disponible en Kaggle:  
📁 [Skin Cancer (PAD-UFES-20)](https://www.kaggle.com/datasets/mahdavi1202/skin-cancer)

## 📊 Descripción del Dataset

El dataset contiene un total de **2,298 imágenes** correspondientes a **1,641 lesiones** de **1,373 pacientes**, abarcando **6 tipos diferentes de condiciones cutáneas**, divididas entre:

- **Cánceres de piel**:
    - BCC: Carcinoma Basocelular (Basal Cell Carcinoma)
    - SCC: Carcinoma de Células Escamosas (Squamous Cell Carcinoma)
    - MEL: Melanoma

- **Otras enfermedades cutáneas**:
    - ACK: Queratosis Actínica (Actinic Keratosis)
    - SEK: Queratosis Seborreica (Seborrheic Keratosis)
    - NEV: Nevus


### 📁 Estructura de los datos

- El dataset original viene comprimido en un `.zip` que contiene:
    - Una carpeta con **todas las imágenes sin clasificar**.
    - Un archivo `.csv` con **metadatos y etiquetas diagnósticas**.

### 🧬 Atributos en los metadatos (CSV)

El CSV contiene **26 atributos** por cada muestra. Algunos de los más relevantes son:

- `patient_id`, `lesion_id`, `img_id`: identificadores únicos.
- `diagnostic`: etiqueta con el tipo de lesión.
- `age`, `gender`, `region`: información del paciente.
- Factores de riesgo como: `smoke`, `drink`, `pesticide`, `skin_cancer_history`, `cancer_history`, etc.
- Características de la lesión: `itch`, `grew`, `hurt`, `changed`, `bleed`, `elevation`, `diameter_1`, `diameter_2`.
- `biopsed`: indica si la muestra fue confirmada por biopsia.

Cerca del **58% de las muestras son biopsiadas** y confirmadas por expertos dermatólogos.

---

## ⚙️ Preprocesamiento de Datos

Dado que las imágenes **no estaban organizadas en carpetas por tipo de cáncer**, se desarrolló un script en Python para clasificar automáticamente las imágenes con base en su `lesion_id` y el diagnóstico asociado.

### 🛠️ Funcionamiento del Script

1. Se lee el archivo `.csv` para construir un **diccionario** con pares `lesion_id: diagnóstico`.
2. Se procesan todas las imágenes, extrayendo el `lesion_id` a partir del nombre de archivo, cuyo formato es:
    ```
    PAT_[patient_id]_[lesion_id]_[img_id].png
    ```

Ejemplo: `PAT_9_17_80.png`  
→ `lesion_id = 17`  
→ `diagnóstico = ACK`  
→ La imagen se mueve a la carpeta `/ACK`

3. Las imágenes se **reorganizan en carpetas**, una por cada diagnóstico (`ACK`, `BCC`, `MEL`, `NEV`, `SEK`, `SCC`).

---

## 📁 División del Dataset

Una vez reorganizadas las imágenes, se realiza la división del dataset en conjuntos de entrenamiento, validación y prueba:

- `train`: 70% de las imágenes.
- `validation`: 10% de las imágenes.
- `test`: 20% de las imágenes.

Cada carpeta (`train`, `validation`, `test`) contiene subcarpetas por tipo de diagnóstico.

---

## ✅ Estado Actual

- ✅ Dataset descargado y explorado
- ✅ Script para organización por diagnóstico implementado
- ✅ División en conjuntos de datos completada


