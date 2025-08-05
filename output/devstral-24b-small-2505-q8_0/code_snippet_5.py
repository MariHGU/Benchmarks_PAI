import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
NUM_FOLDERS = None # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = 'out_data/'
TARGET_COUNT = 300

def check_dataset_balance(output_path=OUTPUT_PATH):
    """
    Checks whether each category (identified by the filename prefix, assumed to be the PLU number)
    in the output folder has the same number of images as the category with the highest count.
    Returns:
    missing_dict (dict): A dictionary where keys are PLU numbers and values are the number of
                         images missing to reach the target count.
    is_balanced (bool): True if every category has reached or exceeded the target count, False otherwise.
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

    # Build a dictionary of missing images per category
    missing_dict = {}
    is_balanced = True
    for category, count in sorted(category_counts.items()):
        missing = TARGET_COUNT - count
        missing_dict[category] = max(0, missing)  # Ensure we don't have negative values
        if missing > 0:
            is_balanced = False

    return missing_dict, is_balanced

def augment_cropped_images(output_path=OUTPUT_PATH, num_folders=None, num_files_per_folder=None):
    """
    Iterates over already-cropped images in the output directory and generates augmentations
    (rotations, horizontal flip, vertical flip, and a combined flip + rotation) to balance the dataset.
    """
    # Check if we need to balance the dataset
    missing_dict, balanced = check_dataset_balance(output_path)
    if balanced:
        print("Dataset is already balanced.")
        return

    all_items = os.listdir(output_path)
    folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]

    # Limit the number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]

    augmentations = {
        'rot90': lambda img: img.rotate(90, expand=True),
        'rot180': lambda img: img.rotate(180, expand=True),
        'rot270': lambda img: img.rotate(270, expand=True),
        'flipH': lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
        'flipV': lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
        'flipH_rot90': lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).rotate(90, expand=True)
    }

    for folder in folders:
        folder_path = os.path.join(output_path, folder)

        # Get all cropped images (files ending with '_cropped.png')
        cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]

        if num_files_per_folder is not None:
            cropped_files = cropped_files[:num_files_per_folder]

        for cropped_file in cropped_files:
            base_name = cropped_file.replace('_cropped.png', '')
            image_path = os.path.join(folder_path, cropped_file)
            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"⚠️ Failed to open image {image_path}: {e}")
                continue

            # Apply augmentations
            for aug_name, aug_func in augmentations.items():
                augmented_img = aug_func(img)
                save_path = os.path.join(folder_path, f"{base_name}_cropped_{aug_name}.png")
                augmented_img.save(save_path)
                print(f"✅ Saved {aug_name} image: {save_path}")

            # Check if we have reached the target count for this category
            if check_dataset_balance(output_path)[1]:
                break

if __name__ == '__main__':
    augment_cropped_images(output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER)