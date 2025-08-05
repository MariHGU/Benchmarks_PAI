import os
from PIL import Image
from collections import defaultdict
import random

# === CONFIGURATION ===
NUM_FOLDERS = None  # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None  # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = 'out_data/'
TARGET_COUNT = 300

def check_dataset_balance(output_path=OUTPUT_PATH):
    """Checks whether each category (PLU) has the same number of images as the category with the highest count."""
    all_files = [f for f in os.listdir(output_path) if f.endswith('.png')]
    category_counts = defaultdict(int)
    
    for filename in all_files:
        parts = filename.split('_')
        if parts:
            category = parts[0]
            category_counts[category] += 1

    if not category_counts:
        print("No images found in the output folder.")
        return {}, True

    max_count = max(category_counts.values())
    missing_dict = {}
    is_balanced = True

    for category, count in sorted(category_counts.items()):
        missing = max_count - count
        missing_dict[category] = missing
        if missing > 0:
            is_balanced = False

    return missing_dict, is_balanced


def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """Augments cropped images in under-represented folders to reach TARGET_COUNT."""
    
    all_items = os.listdir(output_path)
    folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]

    # Limit the number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]

    for folder in folders:
        folder_path = os.path.join(output_path, folder)
        total_png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
        
        # Check current count
        current_count = len(total_png_files)
        needed = TARGET_COUNT - current_count

        if needed <= 0:
            print(f"✅ Folder '{folder}' already has {current_count} images. Skipping.")
            continue

        print(f"🔄 Folder '{folder}' needs {needed} more images.")

        # Get all cropped files to use for augmentation
        cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]
        if num_files_per_folder is not None:
            cropped_files = cropped_files[:num_files_per_folder]

        if not cropped_files:
            print(f"⚠️ No '_cropped.png' files found in folder '{folder}'. Skipping.")
            continue

        # Keep track of augmented images per file to avoid duplication
        processed_files = set()

        for cropped_file in cropped_files:
            base_name = cropped_file.replace('_cropped.png', '')
            image_path = os.path.join(folder_path, cropped_file)

            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"⚠️ Failed to open image {image_path}: {e}")
                continue

            # If we've already augmented enough, skip
            if len(os.listdir(folder_path)) >= TARGET_COUNT:
                break

            # Augmentations: rotations + flips
            augmentations = [
                ("rot90", lambda i: i.rotate(90, expand=True)),
                ("rot180", lambda i: i.rotate(180, expand=True)),
                ("rot270", lambda i: i.rotate(270, expand=True)),
                ("flipH", lambda i: i.transpose(Image.FLIP_LEFT_RIGHT)),
                ("flipV", lambda i: i.transpose(Image.FLIP_TOP_BOTTOM)),
                ("flipH_rot90", lambda i: i.transpose(Image.FLIP_LEFT_RIGHT).rotate(90, expand=True))
            ]

            for aug_name, augment_func in augmentations:
                if len(os.listdir(folder_path)) >= TARGET_COUNT:
                    break

                save_path = os.path.join(folder_path, f"{base_name}_cropped_{aug_name}.png")
                augmented_img = augment_func(img)
                augmented_img.save(save_path)
                print(f"✅ Saved augmented image: {save_path}")

            processed_files.add(cropped_file)

    print("✅ Augmentation complete.")


def balance_dataset(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """Main function to balance dataset by augmenting under-represented folders."""
    missing_dict, is_balanced = check_dataset_balance(output_path=output_path)
    
    if is_balanced:
        print("✅ Dataset already balanced.")
        return

    print("🔍 Balancing dataset...")
    for plu, missing in missing_dict.items():
        if missing > 0:
            folder_path = os.path.join(output_path, plu)
            if not os.path.exists(folder_path):
                print(f"⚠️ Folder {plu} does not exist.")
                continue
            print(f"📄 PLU '{plu}' is missing {missing} images.")

    # Run augmentation to balance dataset
    augment_cropped_images(output_path=output_path, num_folders=num_folders, num_files_per_folder=num_files_per_folder)


if __name__ == '__main__':
    balance_dataset(output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER)