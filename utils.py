import os
import pandas as pd
import re
import shutil
import random
import math


def read_csv(csv_file):
    """
    Read the CSV file and load it into a pandas DataFrame.
    Args:
        csv_file (str): Path to the metadata CSV file
    Returns:
        pd.DataFrame: The loaded metadata dataframe
    """
    df = pd.read_csv(csv_file)

    # Print summary information
    print(f"Unique patient_id values: {df['patient_id'].nunique()}")
    print(f"Rows in the dataframe: {df.shape[0]}")

    return df


def create_diagnostic_directories(output_dir, unique_diagnostics):
    """
    Create directories for each diagnostic category.

    Args:
        output_dir (str): Base output directory
        unique_diagnostics (list): List of unique diagnostic values

    Returns:
        dict: Mapping from diagnosis to directory name
    """
    os.makedirs(output_dir, exist_ok=True)

    # Create directories for each diagnosis and build mapping
    diagnosis_to_dirname = {}
    for diagnosis in unique_diagnostics:
        # Create a valid directory name (replace any problematic characters)
        dirname = re.sub(r'[^\w\s-]', '', diagnosis).strip().replace(' ', '_')
        diagnosis_dir = os.path.join(output_dir, dirname)
        os.makedirs(diagnosis_dir, exist_ok=True)
        diagnosis_to_dirname[diagnosis] = dirname
        print(f"Created directory: {diagnosis_dir}")

    return diagnosis_to_dirname


def organize_images_by_diagnosis(image_dir, output_dir, lesion_to_diagnostic, diagnosis_to_dirname):
    """
    Organize images into directories based on their diagnostic category.

    Args:
        image_dir (str): Directory containing all images
        output_dir (str): Base output directory
        lesion_to_diagnostic (dict): Mapping from lesion_id to diagnostic
        diagnosis_to_dirname (dict): Mapping from diagnosis to directory name

    Returns:
        Counts of (total images processed, successfully moved, errors)
    """
    image_count = 0
    moved_count = 0
    error_count = 0

    # List all image files
    image_files = [f for f in os.listdir(image_dir)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        try:
            # Parse the filename to extract lesion_id
            # Expected format: PAT_[patient_id]_[lesion_id]_[img_id].png
            parts = image_file.split('_')
            if len(parts) >= 3:
                lesion_id = int(parts[2])

                # Get the diagnostic for this lesion
                if lesion_id in lesion_to_diagnostic:
                    diagnostic = lesion_to_diagnostic[lesion_id]

                    # Get the directory name for this diagnostic
                    dirname = diagnosis_to_dirname[diagnostic]
                    target_dir = os.path.join(output_dir, dirname)

                    # Copy the file
                    source_path = os.path.join(image_dir, image_file)
                    target_path = os.path.join(target_dir, image_file)
                    shutil.copy2(source_path, target_path)
                    moved_count += 1
                else:
                    print(f"Warning: No diagnostic found for lesion_id {lesion_id} in file {image_file}")
                    error_count += 1
            else:
                print(f"Warning: Could not parse filename: {image_file}")
                error_count += 1
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
            error_count += 1

        image_count += 1
        if image_count % 100 == 0:
            print(f"Processed {image_count} images, moved {moved_count}, errors {error_count}")

    return image_count, moved_count, error_count


def diagnosis_summary(output_dir, unique_diagnostics, diagnosis_to_dirname):
    """
    Print summary of how many images are in each diagnostic directory.

    Args:
        output_dir (str): Base output directory
        unique_diagnostics (list): List of unique diagnostic values
        diagnosis_to_dirname (dict): Mapping from diagnosis to directory name
    """
    print("\nSummary of images by diagnosis:")
    total_images = 0

    for diagnosis in unique_diagnostics:
        dirname = diagnosis_to_dirname[diagnosis]
        diagnosis_dir = os.path.join(output_dir, dirname)
        files_count = len([f for f in os.listdir(diagnosis_dir)
                           if os.path.isfile(os.path.join(diagnosis_dir, f))])
        total_images += files_count
        print(f"{diagnosis}: {files_count} images")

    print(f"Total: {total_images} images")


def validate_image_organization(output_dir, lesion_to_diagnostic, diagnosis_to_dirname):
    """
    Validate that images are in the correct directories based on their lesion_id.

    Args:
        output_dir (str): Base output directory
        lesion_to_diagnostic (dict): Mapping from lesion_id to diagnostic
        diagnosis_to_dirname (dict): Mapping from diagnosis to directory name

    Returns:
        Counts of (total images checked, correct, incorrect, errors)
    """
    print("\nValidating image organization...")
    total_images = 0
    correct_images = 0
    incorrect_images = 0
    error_images = 0

    # Create reverse mapping from directory name to diagnosis
    dirname_to_diagnosis = {v: k for k, v in diagnosis_to_dirname.items()}

    # Get all directories in the output directory
    dirs = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]

    for dirname in dirs:
        dir_path = os.path.join(output_dir, dirname)
        expected_diagnosis = dirname_to_diagnosis.get(dirname)

        if not expected_diagnosis:
            print(f"Warning: Directory {dirname} does not match any known diagnosis")
            continue

        # Get all images in this directory
        images = [f for f in os.listdir(dir_path)
                  if os.path.isfile(os.path.join(dir_path, f)) and
                  f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for image in images:
            total_images += 1

            try:
                # Parse the filename to extract lesion_id
                parts = image.split('_')
                if len(parts) >= 3:
                    lesion_id = int(parts[2])

                    # Get the expected diagnostic for this lesion
                    if lesion_id in lesion_to_diagnostic:
                        actual_diagnosis = lesion_to_diagnostic[lesion_id]

                        if actual_diagnosis == expected_diagnosis:
                            correct_images += 1
                        else:
                            incorrect_images += 1
                            print(f"Incorrect placement: {image} is in {dirname} but should be in "
                                  f"{diagnosis_to_dirname[actual_diagnosis]}")
                    else:
                        error_images += 1
                        print(f"Warning: No diagnostic found for lesion_id {lesion_id} in file {image}")
                else:
                    error_images += 1
                    print(f"Warning: Could not parse filename: {image}")
            except Exception as e:
                error_images += 1
                print(f"Error validating {image}: {str(e)}")

    print(f"Validation complete: {correct_images}/{total_images} correct, {incorrect_images} incorrect,"
          f"{error_images} errors")
    return total_images, correct_images, incorrect_images, error_images


def create_train_val_test_directories(source_dir, train_dir, val_dir, test_dir):
    """
    Create directory structure for train, validation, and test sets.
    train - 70%
    val - 10%
    test - 20%

    Args:
        source_dir (str): Directory containing the organized dataset
        train_dir (str): Directory for training data
        val_dir (str): Directory for validation data
        test_dir (str): Directory for test data

    Returns:
        list: List of diagnosis directory names
    """
    print("\nCreating train/val/test directory structure...")

    # Create main directories if they don't exist
    for directory in [train_dir, val_dir, test_dir]:
        os.makedirs(directory, exist_ok=True)

    # Get all diagnosis directories
    diagnosis_dirs = [d for d in os.listdir(source_dir)
                      if os.path.isdir(os.path.join(source_dir, d))]

    # Create the same diagnosis directories under each split
    for diagnosis_dir in diagnosis_dirs:
        os.makedirs(os.path.join(train_dir, diagnosis_dir), exist_ok=True)
        os.makedirs(os.path.join(val_dir, diagnosis_dir), exist_ok=True)
        os.makedirs(os.path.join(test_dir, diagnosis_dir), exist_ok=True)

    print(f"Created directory structure for {len(diagnosis_dirs)} diagnosis categories")
    return diagnosis_dirs


def split_dataset(source_dir, train_dir, val_dir, test_dir, diagnosis_dirs,
                  train_ratio=0.7, val_ratio=0.1, test_ratio=0.2, random_seed=42):
    """
    Split the dataset into train, validation, and test sets.

    Args:
        source_dir (str): Directory containing the organized dataset
        train_dir (str): Directory for training data
        val_dir (str): Directory for validation data
        test_dir (str): Directory for test data
        diagnosis_dirs (list): List of diagnosis directory names
        train_ratio (float): Ratio of data for training
        val_ratio (float): Ratio of data for validation
        test_ratio (float): Ratio of data for testing
        random_seed (int): Random seed for reproducibility

    Returns:
        dict: Statistics about the split
    """
    print("\nSplitting dataset into train, validation, and test sets")

    # Set random seed for reproducibility
    random.seed(random_seed)

    # Dictionary to store statistics
    stats = {
        "diagnosis": [],
        "total": [],
        "train": [],
        "val": [],
        "test": []
    }

    # Process each diagnosis directory
    for diagnosis_dir in diagnosis_dirs:
        source_dir_path = os.path.join(source_dir, diagnosis_dir)

        # Get all image files
        image_files = [f for f in os.listdir(source_dir_path)
                       if os.path.isfile(os.path.join(source_dir_path, f)) and
                       f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # Shuffle the files to ensure random distribution
        random.shuffle(image_files)

        # Calculate split sizes
        total_files = len(image_files)
        train_size = math.floor(total_files * train_ratio)
        val_size = math.floor(total_files * val_ratio)
        test_size = math.floor(total_files * test_ratio)

        if train_size + val_size + test_size > total_files:
            raise ValueError("The sum of train, val, and test sizes exceeds the total number of files.")

        # Update statistics
        stats["diagnosis"].append(diagnosis_dir)
        stats["total"].append(total_files)
        stats["train"].append(train_size)
        stats["val"].append(val_size)
        stats["test"].append(test_size)

        # Split the files
        train_files = image_files[:train_size]
        val_files = image_files[train_size:train_size + val_size]
        test_files = image_files[train_size + val_size:]

        # Copy files to their respective directories
        print(f"Processing {diagnosis_dir}...")

        # Helper function to copy files
        def copy_files(files, dest_dir):
            for file in files:
                source_path = os.path.join(source_dir_path, file)
                dest_path = os.path.join(dest_dir, diagnosis_dir, file)
                shutil.copy2(source_path, dest_path)

        print(f"  - Copying {len(train_files)} files to train set")
        copy_files(train_files, train_dir)

        print(f"  - Copying {len(val_files)} files to validation set")
        copy_files(val_files, val_dir)

        print(f"  - Copying {len(test_files)} files to test set")
        copy_files(test_files, test_dir)

    return stats


def create_split_report(stats, base_dir, train_ratio=0.7, val_ratio=0.1, test_ratio=0.2):
    """
    Create a detailed report about the dataset split.

    Args:
        stats (dict): Statistics about the split
        base_dir (str): Base directory where to save the report
        train_ratio (float): Ratio of data for training
        val_ratio (float): Ratio of data for validation
        test_ratio (float): Ratio of data for testing

    Returns:
        str: The report content
    """
    print("\nCreating dataset split report...")

    # Convert stats to DataFrame for easier formatting
    df = pd.DataFrame(stats)

    # Calculate percentages
    df['train_pct'] = (df['train'] / df['total'] * 100).round(1)
    df['val_pct'] = (df['val'] / df['total'] * 100).round(1)
    df['test_pct'] = (df['test'] / df['total'] * 100).round(1)

    # Add totals row
    df.loc['Total'] = df.sum(numeric_only=True)
    df.at['Total', 'diagnosis'] = 'TOTAL'

    # Calculate overall percentages
    total_row = df.loc['Total']
    df.at['Total', 'train_pct'] = (total_row['train'] / total_row['total'] * 100).round(1)
    df.at['Total', 'val_pct'] = (total_row['val'] / total_row['total'] * 100).round(1)
    df.at['Total', 'test_pct'] = (total_row['test'] / total_row['total'] * 100).round(1)

    # Generate report string
    report = "Dataset Split Report\n"
    report += "==================\n\n"
    report += f"Train ratio: {train_ratio:.0%}, Validation ratio: {val_ratio:.0%}, Test ratio: {test_ratio:.0%}\n\n"

    # Add table
    report += df.to_string(
        columns=['diagnosis', 'total', 'train', 'train_pct', 'val', 'val_pct', 'test', 'test_pct'],
        header=['Diagnosis', 'Total', 'Train', 'Train %', 'Val', 'Val %', 'Test', 'Test %'],
        index=False
    )

    # Write report to file
    report_path = os.path.join(base_dir, "split_report.txt")
    with open(report_path, 'w') as f:
        f.write(report)

    print(f"Report saved to {report_path}")
    return report


# Main functions that combine the steps

def organize_dataset(csv_file, image_dir, output_dir):
    """
    Organize images into directories based on their diagnostic category.

    Args:
        csv_file (str): Path to the metadata CSV file
        image_dir (str): Directory containing all images
        output_dir (str): Base output directory
    """
    # Load metadata
    df = read_csv(csv_file)

    # Create mapping from lesion_id to diagnostic
    lesion_to_diagnostic = dict(zip(df['lesion_id'], df['diagnostic']))

    # Get unique diagnostics
    unique_diagnostics = df['diagnostic'].unique()
    print(f"Found {len(unique_diagnostics)} unique diagnoses: {unique_diagnostics}")

    # Create directories for each diagnosis
    diagnosis_to_dirname = create_diagnostic_directories(output_dir, unique_diagnostics)

    # Organize images by diagnosis
    image_count, moved_count, error_count = organize_images_by_diagnosis(
        image_dir, output_dir, lesion_to_diagnostic, diagnosis_to_dirname)

    print(f"Finished processing {image_count} images.")
    print(f"Successfully moved {moved_count} images to their diagnosis directories.")
    print(f"Encountered {error_count} errors.")

    # Print summary of files in each directory
    diagnosis_summary(output_dir, unique_diagnostics, diagnosis_to_dirname)

    # Validate image organization
    validate_image_organization(output_dir, lesion_to_diagnostic, diagnosis_to_dirname)

    return lesion_to_diagnostic, diagnosis_to_dirname


def create_train_val_test_split(source_dir, train_dir, val_dir, test_dir,
                                train_ratio=0.7, val_ratio=0.1, test_ratio=0.2, random_seed=42):
    """
    Create train, validation, and test splits from the organized dataset.

    Args:
        source_dir (str): Directory containing the organized dataset
        train_dir (str): Directory for training data
        val_dir (str): Directory for validation data
        test_dir (str): Directory for test data
        train_ratio (float): Ratio of data for training
        val_ratio (float): Ratio of data for validation
        test_ratio (float): Ratio of data for testing
        random_seed (int): Random seed for reproducibility
    """
    # Create directory structure
    diagnosis_dirs = create_train_val_test_directories(source_dir, train_dir, val_dir, test_dir)

    # Split the dataset
    stats = split_dataset(source_dir, train_dir, val_dir, test_dir, diagnosis_dirs,
                          train_ratio, val_ratio, test_ratio, random_seed)

    # Create split report
    report = crea3te_split_report(stats, os.path.dirname(train_dir), train_ratio, val_ratio, test_ratio)

    print(report)


# Example usage
def main():

    # Default paths
    csv_file = 'data/metadata.csv'
    image_dir = 'data/full_images'
    organized_dir = 'data/organized_images'
    train_dir = 'data/train'
    val_dir = 'data/validation'
    test_dir = 'data/test'

    # Step 1: Organize the dataset by diagnosis
    organize_dataset(csv_file, image_dir, organized_dir)

    # Step 2: Create train/val/test splits
    create_train_val_test_split(organized_dir, train_dir, val_dir, test_dir)


if __name__ == "__main__":
    main()
