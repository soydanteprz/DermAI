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

Dado que las imágenes **no estaban organizadas en carpetas por tipo de cáncer**, se desarrolló el script `utils.py` para **reorganizar las imágenes** en carpetas según su diagnóstico.

1. Se lee el archivo `metadata.csv` para construir un **diccionario** con pares `lesion_id: diagnóstico`.
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

La carpeta data contiene la siguiente estructura:

```
data/
├── metadata.csv
├── split_report.txt
├── full_images
├── organized_images
├── train/
│   ├── ACK/
│   ├── BCC/
│   ├── MEL/
│   ├── NEV/
│   ├── SEK/
│   └── SCC/
├── validation/
│   ├── ACK/
│   ├── BCC/
│   ├── MEL/
│   ├── NEV/
│   ├── SEK/
│   └── SCC/
└── test/
    ├── ACK/
    ├── BCC/
    ├── MEL/
    ├── NEV/
    ├── SEK/
    └── SCC/
```
### 📊 Reporte de División
El archivo `split_report.txt` contiene un resumen de la división del dataset, mostrando el número de imágenes por tipo de diagnóstico en cada conjunto (train, validation, test).
La carpeta `full_images` contiene todas las imágenes originales sin clasificar, mientras que `organized_images` contiene las imágenes reorganizadas por diagnóstico.
Despues las imágenes se dividen en conjuntos de entrenamiento, validación y prueba, asegurando que cada conjunto tenga una representación equitativa de cada tipo de diagnóstico.

> ⚠️ **Nota importante**  
En el GitHub solamente se puede encontrar dentro de la carpeta `data` el archivo `metadata.csv`, el archivo `split_report.txt` por razones de espacio, pero en el siguiente link a Drive se wncuentra el resto de los archivos:
[Google Drive](https://drive.google.com/drive/folders/1nR3f4mr7ylwR_OyzVkAkjps9zQubiuI6?usp=sharing)
>

## 🧠 Data Augmentation y Entrenamiento del Modelo

### 📈 Aumento de Datos

Para mejorar el rendimiento del modelo de clasificación, se aplicaron técnicas de **data augmentation** utilizando el notebook [`data_augmentation.ipynb`](./data_augmentation.ipynb).  
En este script:

- Se genera un **diccionario anidado** que contiene la información actual de cada carpeta (una por diagnóstico) y la **cantidad de imágenes** disponibles.
- Se evalúa el **balance del dataset** para determinar qué clases necesitan mayor augmentación.
- Se aplican transformaciones como rotaciones, zoom, flips horizontales y verticales, entre otras, para aumentar la diversidad del conjunto de datos de entrenamiento sin necesidad de recolectar más imágenes.

---

### 🧪 Modelo de Clasificación CNN

El modelo se define y entrena en el notebook [`cnn_dermai.ipynb`](./cnn_dermai.ipynb), inspirado en el artículo científico:

> 📄 *Skin cancer classification using convolutional neural networks*  
> [IOP Science, 2020](https://iopscience.iop.org/article/10.1088/1757-899X/982/1/012005/pdf)

En este notebook:

- Se construye una arquitectura **CNN personalizada** basada en la propuesta del paper.
- Se entrena el modelo con el dataset de imágenes dermatológicas reorganizado.
- Se utilizan técnicas como:
  - Normalización de imágenes.
  - Callbacks como `ModelCheckpoint` y `EarlyStopping`.
- Al finalizar el entrenamiento, se guarda el modelo entrenado en el archivo `modelo_dermai.h5`, para su uso posterior en inferencia o despliegue.

## ✅ Estado Actual

- ✅ Dataset descargado y explorado
- ✅ Script para organización por diagnóstico implementado
- ✅ División en conjuntos de datos completada
- ✅ Data augmentation aplicado
- ✅ Modelo CNN definido y entrenado (No es el definitivo, se puede mejorar)
- ✅ Modelo guardado en formato `.h5`

---

## 👤 Autor

- **Dante David Pérez Pérez A01709226**

Uso de Data augmentation para mejorar el rendimiento del modelo de clasificación de imágenes, el script data_augmentation.ipynb creamos un diccionario de diccionario donde tiene la informacion actual de cada carpeta y la cantidad de imagenes que tiene.

Despues en cnn_dermai.ipynb se crea el modelo basado en el papel Skin cancer classification https://iopscience.iop.org/article/10.1088/1757-899X/982/1/012005/pdf
y se entrena con el dataset de imagenes de cancer de piel, al final se guarda el modelo en un archivo .h5 para su uso posterior.




def create_model():
"""Create CNN model based on research paper architecture with Mac M3 Pro GPU optimization"""

    print("CREATING CNN MODEL")
    print("-" * 40)

    strategy = tf.distribute.get_strategy()

    with strategy.scope():
        model = models.Sequential([
            # Input layer - adjusted to 150x150 instead of 128x128 to match your dataset
            layers.Input(shape=(128, 128, 3), name='input_layer'),

            layers.Conv2D(16, (3, 3), padding='same', name='conv1'),
            layers.BatchNormalization(name='batchnorm1'),
            layers.ReLU(name='relu1'),
            layers.MaxPooling2D((2, 2), name='maxpool1'),
            layers.Dropout(0.2, name='dropout1'),

            # Second Convolution Block
            layers.Conv2D(32, (3, 3), padding='same', name='conv2'),
            layers.BatchNormalization(name='batchnorm2'),
            layers.ReLU(name='relu2'),
            layers.MaxPooling2D((2, 2), name='maxpool2'),
            layers.Dropout(0.2, name='dropout2'),

            # Third Convolution Block
            layers.Conv2D(64, (3, 3), padding='same', name='conv3'),
            layers.BatchNormalization(name='batchnorm3'),
            layers.ReLU(name='relu3'),
            layers.MaxPooling2D((2, 2), name='maxpool3'),
            layers.Dropout(0.3, name='dropout3'),

            # Bloque Convolucional 3 (nuevo)
            layers.Conv2D(128, (3, 3), padding='same'),
            layers.BatchNormalization(),
            layers.ReLU(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.4),

            layers.Flatten(),
            layers.Dense(128, activation='relu'),  # Capa densa intermedia
            layers.Dropout(0.5),
            layers.Dense(6, activation='softmax')
        ])

        # Optimized learning rate for GPU training (matching paper style)
        initial_lr = 0.001

        # Compile model - using paper-style optimizer
        model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizers.Adam(learning_rate=initial_lr),
            metrics=['accuracy']
        )

    print(f"📊 Total parameters: {model.count_params():,}")
    print(f"🎯 Optimized for: {'Mac M3 Pro GPU' if gpu_available else 'CPU'}")
    print(f"📈 Initial learning rate: {initial_lr}")

    # Display model summary
    model.summary()
    print()

    return model


Epoch 60/60
1/93 ━━━━━━━━━━━━━━━━━━━━ 5s 65ms/step - accuracy: 0.2500 - loss: 6.2239
Epoch 60: val_accuracy did not improve from 0.31250
93/93 ━━━━━━━━━━━━━━━━━━━━ 4s 47ms/step - accuracy: 0.2500 - loss: 6.2239 - val_accuracy: 0.2232 - val_loss: 6.0415 - learning_rate: 1.0000e-08
