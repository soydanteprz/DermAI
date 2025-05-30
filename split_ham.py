import os
import shutil
import random
from pathlib import Path
from collections import defaultdict

def split_ham10000_dataset(source_folder, output_folder, train_ratio=0.7, val_ratio=0.1, test_ratio=0.2, copy_files=True):
    """
    Divide el dataset HAM10000 en train/validation/test manteniendo la distribución por clases

    Args:
        source_folder: Carpeta con las 6 clases organizadas (HAM10000_organized)
        output_folder: Carpeta donde crear train/validation/test
        train_ratio: Porcentaje para entrenamiento (default: 0.7)
        val_ratio: Porcentaje para validación (default: 0.1)
        test_ratio: Porcentaje para prueba (default: 0.2)
        copy_files: True para copiar, False para mover archivos
    """

    # Verificar que los ratios sumen 1.0
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 0.001:
        print(f"❌ Error: Los ratios deben sumar 1.0")
        print(f"   Train: {train_ratio}, Val: {val_ratio}, Test: {test_ratio}")
        print(f"   Suma: {train_ratio + val_ratio + test_ratio}")
        return

    source_path = Path(source_folder)
    output_path = Path(output_folder)

    # Verificar que la carpeta fuente existe
    if not source_path.exists():
        print(f"❌ Error: La carpeta {source_folder} no existe")
        return

    # Obtener las clases (carpetas) disponibles
    class_folders = [f for f in source_path.iterdir() if f.is_dir()]

    if not class_folders:
        print(f"❌ Error: No se encontraron carpetas de clases en {source_folder}")
        return

    print(f"📁 Carpeta fuente: {source_folder}")
    print(f"📁 Carpeta destino: {output_folder}")
    print(f"📊 Distribución: Train {train_ratio*100}% | Val {val_ratio*100}% | Test {test_ratio*100}%")
    print(f"🔄 Modo: {'Copiar' if copy_files else 'Mover'} archivos")
    print(f"🎯 Clases encontradas: {len(class_folders)}")

    # Crear estructura de carpetas
    splits = ['train', 'validation', 'test']

    print(f"\n📁 Creando estructura de carpetas...")
    for split in splits:
        split_path = output_path / split
        split_path.mkdir(parents=True, exist_ok=True)

        for class_folder in class_folders:
            class_name = class_folder.name
            class_split_path = split_path / class_name
            class_split_path.mkdir(exist_ok=True)
            print(f"   Creada: {split}/{class_name}/")

    # Estadísticas para el resumen final
    split_stats = defaultdict(lambda: defaultdict(int))
    total_stats = defaultdict(int)

    # Procesar cada clase
    print(f"\n🔄 Procesando clases...")

    for class_folder in class_folders:
        class_name = class_folder.name
        print(f"\n📂 Procesando clase: {class_name}")

        # Obtener todas las imágenes de la clase
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        all_images = []

        for ext in image_extensions:
            all_images.extend(list(class_folder.glob(ext)))

        total_images = len(all_images)
        print(f"   📊 Total imágenes: {total_images}")

        if total_images == 0:
            print(f"   ⚠️  No se encontraron imágenes en {class_name}")
            continue

        # Calcular distribución
        train_count = int(total_images * train_ratio)
        val_count = int(total_images * val_ratio)
        test_count = total_images - train_count - val_count  # El resto va a test

        print(f"   🎯 Distribución: Train:{train_count} | Val:{val_count} | Test:{test_count}")

        # Mezclar imágenes aleatoriamente
        random.seed(42)  # Para reproducibilidad
        random.shuffle(all_images)

        # Dividir imágenes
        train_images = all_images[:train_count]
        val_images = all_images[train_count:train_count + val_count]
        test_images = all_images[train_count + val_count:]

        # Copiar/mover imágenes a cada split
        splits_data = {
            'train': train_images,
            'validation': val_images,
            'test': test_images
        }

        for split_name, images in splits_data.items():
            if not images:
                continue

            dest_folder = output_path / split_name / class_name

            print(f"   📦 {split_name}: {len(images)} imágenes")

            for i, img_path in enumerate(images):
                try:
                    dest_path = dest_folder / img_path.name

                    if copy_files:
                        shutil.copy2(img_path, dest_path)
                    else:
                        shutil.move(str(img_path), str(dest_path))

                    # Progreso cada 100 imágenes
                    if (i + 1) % 100 == 0:
                        print(f"      Procesadas: {i + 1}/{len(images)}")

                except Exception as e:
                    print(f"   ❌ Error procesando {img_path.name}: {e}")

            # Actualizar estadísticas
            split_stats[split_name][class_name] = len(images)
            total_stats[split_name] += len(images)

    # Resumen final
    print(f"\n🎉 ¡División completada!")
    print(f"\n📊 RESUMEN FINAL:")

    print(f"\n📈 Por split:")
    for split_name in ['train', 'validation', 'test']:
        total = total_stats[split_name]
        percentage = (total / sum(total_stats.values())) * 100 if sum(total_stats.values()) > 0 else 0
        print(f"   {split_name.upper()}: {total} imágenes ({percentage:.1f}%)")

    print(f"\n📈 Por clase y split:")
    print(f"{'Clase':<10} {'Train':<8} {'Val':<8} {'Test':<8} {'Total':<8}")
    print("-" * 50)

    for class_folder in sorted(class_folders, key=lambda x: x.name):
        class_name = class_folder.name
        train_count = split_stats['train'][class_name]
        val_count = split_stats['validation'][class_name]
        test_count = split_stats['test'][class_name]
        total_count = train_count + val_count + test_count

        print(f"{class_name:<10} {train_count:<8} {val_count:<8} {test_count:<8} {total_count:<8}")

    # Verificar estructura final
    print(f"\n📁 Estructura final creada:")
    for split in splits:
        split_path = output_path / split
        print(f"   {split}/")
        for class_folder in sorted(class_folders, key=lambda x: x.name):
            class_name = class_folder.name
            class_path = split_path / class_name
            if class_path.exists():
                count = len(list(class_path.glob('*')))
                print(f"      ├── {class_name}/ ({count} imágenes)")

    print(f"\n✅ Dataset dividido exitosamente en: {output_folder}")


# Configuración - MODIFICA ESTAS RUTAS
if __name__ == "__main__":

    # RUTA A TU CARPETA ORGANIZADA (HAM10000_organized)
    source_directory = "data/HAM10000_organized"

    # CARPETA DONDE CREAR TRAIN/VALIDATION/TEST
    output_directory = "HAM10000_split"

    # DISTRIBUCIÓN (deben sumar 1.0)
    train_percentage = 0.7   # 70%
    val_percentage = 0.1     # 10%
    test_percentage = 0.2    # 20%

    # COPIAR O MOVER ARCHIVOS
    copy_files = True  # True = copiar (mantiene originales), False = mover

    print("🚀 Iniciando división del dataset HAM10000...")
    print(f"📁 Desde: {source_directory}")
    print(f"📁 Hacia: {output_directory}")
    print(f"📊 Train: {train_percentage*100}% | Val: {val_percentage*100}% | Test: {test_percentage*100}%")

    # Ejecutar división
    split_ham10000_dataset(
        source_folder=source_directory,
        output_folder=output_directory,
        train_ratio=train_percentage,
        val_ratio=val_percentage,
        test_ratio=test_percentage,
        copy_files=copy_files
    )

    print("\n🎊 ¡División del dataset completada!")
