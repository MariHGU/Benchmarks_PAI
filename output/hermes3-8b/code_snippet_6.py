import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
NUM_FOLDERS = None  # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None  # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = 'out_data/'

def check_dataset_balance(output_path=OUTPUT_PATH):
    """
    Checks whether each category (identified by the filename prefix, assumed to be the PLU number) in the output
    folder has the same number of images as the category with the highest count.
    Returns:
    missing_dict (dict): A dictionary where keys are PLU numbers and values are the number of images missing to reach the maximum count.
    is_balanced (bool): True if every category has the maximum count, False otherwise.
    """
    # List all PNG files in the output folder
    all_files = [f for f in os.listdir(output_path) if f.endswith('.png')]

    # Count images per category (assumes category is the first part of the filename before an underscore)
    category_counts = defaultdict(int)
    for filename in all_files:
        parts = filename.split('_')
        if parts:
            category = parts[0]
            category_counts[category] += 1

    if not category_counts:
        print("No images found in the output folder.")
        return {}, True

    # Find the maximum image count among categories
    max_count = max(category_counts.values())

    # Build a dictionary of missing images per category
    missing_dict = {}
    is_balanced = True
    for category, count in sorted(category_counts.items()):
        missing = 300 - count  # Change the target count to 300
        missing_dict[category] = missing
        if missing > 0:
            is_balanced = False

    return missing_dict, is_balanced


def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """
    Iterates over already-cropped images in the output directory and generates augmentations (rotations,
    horizontal flip, vertical flip, and a combined flip + rotation) only if the folder has less than 200 PNG images.
    """
    all_items = os.listdir(output_path)
    folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]

    # Limit the number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]

    for folder in folders:
        folder_path = os.path.join(output_path, folder)
        
        # Check if the current folder needs more images to reach 300
        total_png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
        missing_images = 300 - len(total_png_files)

        if missing_images <= 0:
            continue
        
        cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]
        
        # Add augmented images until the folder has at least 300 PNG files
        while missing_images > 0:
            augment_cropped_images(folder_path)
            total_png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
            missing_images = 300 - len(total_png_files)

    print(f"Folder '{folder}' has been balanced with at least 300 images.")


if __name__ == '__main__':
    dict_change, balanced = check_dataset_balance(output_path=OUTPUT_PATH)
    
    # Check if the dataset is currently balanced and skip augmentation if it is
    if not balanced:
        augment_cropped_images(output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER)