import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import defaultdict, Counter
import pandas as pd

def analyze_image_properties(train_dir):
    """Analyze all images in the training directory to understand their properties"""

    results = {
        'class_name': [],
        'filename': [],
        'width': [],
        'height': [],
        'aspect_ratio': [],
        'total_pixels': [],
        'file_size_mb': []
    }

    aspect_ratios_by_class = defaultdict(list)
    sizes_by_class = defaultdict(list)

    print("🔍 ANALYZING YOUR CURRENT IMAGES...")
    print("=" * 60)

    for class_name in os.listdir(train_dir):
        class_path = os.path.join(train_dir, class_name)
        if not os.path.isdir(class_path):
            continue

        print(f"\n📁 Analyzing class: {class_name}")

        image_files = [f for f in os.listdir(class_path)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

        class_widths = []
        class_heights = []
        class_aspects = []

        for i, img_file in enumerate(image_files[:5]):  # Sample first 5 images for quick analysis
            try:
                img_path = os.path.join(class_path, img_file)

                # Get file size
                file_size_mb = os.path.getsize(img_path) / (1024 * 1024)

                # Open image and get dimensions
                with Image.open(img_path) as img:
                    width, height = img.size
                    aspect_ratio = width / height
                    total_pixels = width * height

                    # Store results
                    results['class_name'].append(class_name)
                    results['filename'].append(img_file)
                    results['width'].append(width)
                    results['height'].append(height)
                    results['aspect_ratio'].append(aspect_ratio)
                    results['total_pixels'].append(total_pixels)
                    results['file_size_mb'].append(file_size_mb)

                    class_widths.append(width)
                    class_heights.append(height)
                    class_aspects.append(aspect_ratio)

            except Exception as e:
                print(f"   ⚠️ Error reading {img_file}: {e}")

        if class_aspects:
            avg_aspect = np.mean(class_aspects)
            min_aspect = min(class_aspects)
            max_aspect = max(class_aspects)

            print(f"   📏 Dimensions (W×H): {min(class_widths)}×{min(class_heights)} to {max(class_widths)}×{max(class_heights)}")
            print(f"   📐 Aspect ratios: {min_aspect:.2f} to {max_aspect:.2f} (avg: {avg_aspect:.2f})")

            aspect_ratios_by_class[class_name] = class_aspects
            sizes_by_class[class_name] = list(zip(class_widths, class_heights))

    # Convert to DataFrame for analysis
    df = pd.DataFrame(results)

    return df, aspect_ratios_by_class, sizes_by_class

def plot_aspect_ratio_analysis(df, aspect_ratios_by_class):
    """Create visualizations of aspect ratio analysis"""

    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # 1. Aspect ratio distribution by class
    classes = list(aspect_ratios_by_class.keys())
    colors = plt.cm.Set3(np.linspace(0, 1, len(classes)))

    for i, (class_name, aspects) in enumerate(aspect_ratios_by_class.items()):
        ax1.hist(aspects, bins=10, alpha=0.7, label=class_name, color=colors[i])

    ax1.set_xlabel('Aspect Ratio (Width/Height)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Aspect Ratio Distribution by Class')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Image dimensions scatter plot
    for class_name in classes:
        class_data = df[df['class_name'] == class_name]
        ax2.scatter(class_data['width'], class_data['height'],
                    label=class_name, alpha=0.7, s=50)

    ax2.set_xlabel('Width (pixels)')
    ax2.set_ylabel('Height (pixels)')
    ax2.set_title('Image Dimensions by Class')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Total pixels distribution
    ax3.boxplot([df[df['class_name'] == cls]['total_pixels'].values
                 for cls in classes], labels=classes)
    ax3.set_ylabel('Total Pixels')
    ax3.set_title('Image Size Distribution by Class')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3)

    # 4. File size distribution
    ax4.boxplot([df[df['class_name'] == cls]['file_size_mb'].values
                 for cls in classes], labels=classes)
    ax4.set_ylabel('File Size (MB)')
    ax4.set_title('File Size Distribution by Class')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def analyze_aspect_ratio_impact():
    """Analyze the impact of different resizing strategies"""

    print("\n🎯 RESIZING STRATEGY ANALYSIS")
    print("=" * 60)

    # Common aspect ratios in medical imaging
    common_ratios = {
        "Square (1:1)": 1.0,
        "Standard Photo (4:3)": 4/3,
        "Widescreen (16:9)": 16/9,
        "Portrait (3:4)": 3/4,
        "Medical Standard (3:2)": 3/2
    }

    print("📐 Common aspect ratios:")
    for name, ratio in common_ratios.items():
        print(f"   {name}: {ratio:.2f}")

    print("\n🔄 RESIZING OPTIONS:")
    print("\n1. 🎯 KEEP ORIGINAL ASPECT RATIOS (Recommended for medical images)")
    print("   ✅ Pros:")
    print("      - Preserves original image proportions")
    print("      - No distortion of lesions/features")
    print("      - Maintains medical accuracy")
    print("   ❌ Cons:")
    print("      - Variable input sizes for neural network")
    print("      - Requires padding or cropping")
    print("      - More complex data pipeline")

    print("\n2. 🔲 FORCE SQUARE (150×150) - Current approach")
    print("   ✅ Pros:")
    print("      - Uniform input size for neural network")
    print("      - Simpler data pipeline")
    print("      - Faster training")
    print("   ❌ Cons:")
    print("      - May stretch/distort images")
    print("      - Could alter lesion appearance")
    print("      - Loss of original proportions")

    print("\n3. 🎭 SMART RESIZE WITH PADDING")
    print("   ✅ Pros:")
    print("      - Preserves aspect ratio")
    print("      - Uniform output size")
    print("      - No distortion")
    print("   ❌ Cons:")
    print("      - Adds black bars (padding)")
    print("      - Slightly more complex")

    print("\n4. 🔍 CENTER CROP TO SQUARE")
    print("   ✅ Pros:")
    print("      - No distortion")
    print("      - Uniform square output")
    print("   ❌ Cons:")
    print("      - May lose important edge information")
    print("      - Could crop out lesions")

def recommend_strategy(df, aspect_ratios_by_class):
    """Provide recommendations based on the analysis"""

    print("\n💡 RECOMMENDATIONS BASED ON YOUR DATA:")
    print("=" * 60)

    # Calculate statistics
    all_aspects = []
    for aspects in aspect_ratios_by_class.values():
        all_aspects.extend(aspects)

    if not all_aspects:
        print("⚠️ No image data found for analysis")
        return

    avg_aspect = np.mean(all_aspects)
    std_aspect = np.std(all_aspects)
    min_aspect = min(all_aspects)
    max_aspect = max(all_aspects)

    print(f"📊 Your images statistics:")
    print(f"   Average aspect ratio: {avg_aspect:.2f}")
    print(f"   Standard deviation: {std_aspect:.2f}")
    print(f"   Range: {min_aspect:.2f} to {max_aspect:.2f}")

    # Make recommendation
    if std_aspect < 0.1:  # Very consistent aspect ratios
        print(f"\n🎯 RECOMMENDATION: SMART RESIZE WITH PADDING")
        print(f"   Your images have very consistent aspect ratios (std: {std_aspect:.2f})")
        print(f"   This preserves the medical accuracy while maintaining uniform size")

    elif abs(avg_aspect - 1.0) < 0.2:  # Already close to square
        print(f"\n🎯 RECOMMENDATION: CURRENT APPROACH (Force Square) is GOOD")
        print(f"   Your images are already close to square (avg: {avg_aspect:.2f})")
        print(f"   Minimal distortion expected")

    else:  # Variable aspect ratios
        print(f"\n🎯 RECOMMENDATION: SMART RESIZE WITH PADDING")
        print(f"   Your images have variable aspect ratios (std: {std_aspect:.2f})")
        print(f"   Smart resize will preserve medical features better")

# Run the analysis
def main():
    # Set your train directory path
    train_dir = os.path.join(os.getcwd(), 'data', 'train')

    if not os.path.exists(train_dir):
        print("⚠️ Train directory not found. Please check the path:")
        print(f"   Looking for: {train_dir}")
        print("   Current directory:", os.getcwd())
        return

    # Analyze current images
    df, aspect_ratios_by_class, sizes_by_class = analyze_image_properties(train_dir)

    if df.empty:
        print("⚠️ No images found for analysis")
        return

    # Create visualizations
    plot_aspect_ratio_analysis(df, aspect_ratios_by_class)

    # Show detailed statistics
    print("\n📋 DETAILED STATISTICS:")
    print("=" * 60)
    print(df.groupby('class_name').agg({
        'width': ['min', 'max', 'mean'],
        'height': ['min', 'max', 'mean'],
        'aspect_ratio': ['min', 'max', 'mean', 'std'],
        'file_size_mb': ['min', 'max', 'mean']
    }).round(2))

    # Provide analysis and recommendations
    analyze_aspect_ratio_impact()
    recommend_strategy(df, aspect_ratios_by_class)

    return df, aspect_ratios_by_class

# Run the analysis
if __name__ == "__main__":
    df, aspect_ratios = main()
