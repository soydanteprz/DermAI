# Proyecto: Detección de Cáncer en la Piel por Clasificación de Imágenes

Este proyecto tiene como objetivo detectar cáncer en la piel a partir de imágenes de lesiones cutáneas utilizando técnicas de clasificación de imágenes. 
## 📊 Descripción del Dataset


- **Cánceres de piel**:
    - BCC: Carcinoma Basocelular (Basal Cell Carcinoma)
    - SCC: Carcinoma de Células Escamosas (Squamous Cell Carcinoma)
    - MEL: Melanoma

- **Otras enfermedades cutáneas**:
    - ACK: Queratosis Actínica (Actinic Keratosis)
    - SEK: Queratosis Seborreica (Seborrheic Keratosis)
    - NEV: Nevus

## 📁 División del Dataset

Una vez reorganizadas las imágenes, se realiza la división del dataset en conjuntos de entrenamiento, validación y prueba:

- `train`: 70% de las imágenes.
- `validation`: 10% de las imágenes.
- `test`: 20% de las imágenes.

Cada carpeta (`train`, `validation`, `test`) contiene subcarpetas por tipo de diagnóstico.


# Arquitecturas Implementadas
Utilice 6 papers para implementar 6 modelos diferentes adaptados a mis necesidades como las dimenciones de mis images, cantidad de images, etc.
Estos dos modelos fueron lo que mejor funcionaron pero hubo un problema porque al anadir mas images a las clases MEL, NEV Y SEK el accurracy disminuyo.
### 1. Modelo basado en MobileNetV2
Basado en este paper
[CNN Comparative Analysis for Skin Cancer Classification](https://ieeexplore.ieee.org/document/9984324)

### 2. Modelo CNN Personalizado

Basado en este paper [Skin lesion classification of dermoscopic images using machine learning and convolutional neural network](https://www.nature.com/articles/s41598-022-22644-9)


Mas informacion en el Articulo: [Detección de Cáncer de Piel con Redes Neuronales Convolucionales: Comparación de Arquitecturas Usando el Dataset HAM10000 por Dante Pérez](CancerPielCNN.pdf)
---

## 👤 Autor

- **Dante David Pérez Pérez A01709226**
- [Dataset] (https://www.kaggle.com/datasets/danteprez/skincancer-dataset-ham1000-prime/data) 
Descarga el dataset y crea una carpeta dentro `Data` llamada `HAM10000_split` ahi coloca las carpetas `train`, `validation` y `test`
