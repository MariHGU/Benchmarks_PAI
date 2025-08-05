import os
from PIL import Image
from collections import defaultdict
import random

# === CONFIGURATION ===
NUM_FOLDERS = None # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None # Set to None to process all cropped images per folder or a specific number (e.g., 300)
OUTPUT_PATH = 'out_data/'
TARGET_IMAGES_PER_CATEGORY = 300

def check_dataset_balance(output_path=OUTPUT_PATH):
    """ Checks whether each category (identified by the filename prefix, assumed to be the PLU number) in the output folder has the same number of images as the target count.
    
    Returns:
        missing_dict (dict): A dictionary where keys are PLU numbers and values are the number of images missing to reach the target count.
        is_balanced (bool): True if every category has the target count, False otherwise.
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
        missing = TARGET_IMAGES_PER_CATEGORY - count
        if missing > 0:
            is_balanced = False
        missing_dict[category] = max(0, missing)
    
    return missing_dict, is_balanced

def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """ Iterates over already-cropped images in the output directory and generates augmentations (rotations, horizontal flip, vertical flip, and a combined flip + rotation) until each category reaches TARGET_IMAGES_PER_CATEGORY.
    
    Args:
        output_path: Path to the directory containing cropped images
        num_folders: Maximum number of folders to process
        num_files_per_folder: Maximum number of files to process per folder
    
    Returns:
        bool: True if augmentation was successful, False otherwise
    """
    try:
        # Check current balance and get missing counts
        missing_dict, is_balanced = check_dataset_balance(output_path)
        
        if is_balanced:
            print("Dataset is already balanced!")
            return True
        
        all_items = os.listdir(output_path)
        folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]
        
        # Limit the number of folders if specified
        if num_folders is not None:
            folders = folders[:num_folders]
            
        for folder in folders:
            folder_path = os.path.join(output_path, folder)
            
            # Get all cropped images (files ending with '_cropped.png')
            cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]
            
            if num_files_per_folder is not None:
                cropped_files = cropped_files[:num_files_per_folder]
                
            category = folder.split('_')[0]  # Get the PLU number from folder name
            missing_images = missing_dict[category]
            
            if missing_images <= 0:
                continue
                
            augmentations_needed = missing_images // 4 + (1 if missing_images % 4 > 0 else 0)
            files_to_augment = random.sample(cropped_files, min(augmentations_needed, len(cropped_files)))
            
            for cropped_file in files_to_augment:
                base_name = cropped_file.replace('_cropped.png', '')
                image_path = os.path.join(folder_path, cropped_file)
                
                try:
                    img = Image.open(image_path)
                except Exception as e:
                    print(f"⚠️ Failed to open image {image_path}: {e}")
                    continue
                
                # --- Augmentations ---
                # 1. Rotations (90°, 180°, 270°)
                for angle in [90, 180, 270]:
                    rotated_img = img.rotate(angle, expand=True)
                    rotated_save_path = os.path.join(folder_path, f"{base_name}_cropped_rot{angle}.png")
                    rotated_img.save(rotated_save_path)
                    print(f"✅ Saved rotated {angle}° image: {rotated_save_path}")
                
                # 2. Horizontal Flip
                flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT)
                flipped_h_save_path = os.path.join(folder_path, f"{base_name}_cropped_flipH.png")
                flipped_h.save(flipped_h_save_path)
                print(f"✅ Saved horizontal flip image: {flipped_h_save_path}")
                
        return True
    
    except Exception as e:
        print(f"Error during augmentation: {e}")
        return False

if __name__ == '__main__':
    dict_change, balanced = check_dataset_balance(output_path=OUTPUT_PATH)
    
    if not balanced:
        print("Dataset is not balanced. Starting augmentation...")
        success = augment_cropped_images(
            output_path=OUTPUT_PATH,
            num_folders=NUM_FOLDERS,
            num_files_per_folder=NUM_FILES_PER_FOLDER
        )
        
        if success:
            new_dict_change, new_balanced = check_dataset_balance(output_path=OUTPUT_PATH)
            print("Augmentation completed. New balance:")
            for category, count in sorted(new_dict_change.items()):
                print(f"Category {category}: {count} images")
    else:
        print("Dataset is already balanced!")