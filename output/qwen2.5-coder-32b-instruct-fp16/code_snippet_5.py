import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
NUM_FOLDERS = None  # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None  # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = 'out_data/'
TARGET_IMAGES_PER_CATEGORY = 300

def check_dataset_balance(output_path=OUTPUT_PATH):
    """ Checks whether each category (identified by the filename prefix, assumed to be the PLU number) in the output folder has the same number of images as the category with the highest count. Returns: missing_dict (dict): A dictionary where keys are PLU numbers and values are the number of images missing to reach the maximum count. is_balanced (bool): True if every category has the maximum count, False otherwise. """
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
        missing = max_count - count
        missing_dict[category] = missing if missing > 0 else 0
        if missing > 0:
            is_balanced = False
    
    return missing_dict, is_balanced

def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """ Iterates over already-cropped images in the output directory and generates augmentations (rotations, horizontal flip, vertical flip, and a combined flip + rotation) until each category has around 300 images. """
    all_items = os.listdir(output_path)
    folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]
    
    # Limit the number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]
    
    missing_dict, _ = check_dataset_balance(output_path=output_path)
    
    for folder in folders:
        folder_path = os.path.join(output_path, folder)
        
        # Count total PNG files in the folder
        total_png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
        current_count = len(total_png_files)
        
        # Get all cropped images (files ending with '_cropped.png')
        cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]
        
        if num_files_per_folder is not None:
            cropped_files = cropped_files[:num_files_per_folder]
        
        category = folder  # Assuming the folder name is the PLU code
        additional_needed = TARGET_IMAGES_PER_CATEGORY - current_count
        
        print(f"Processing folder '{folder}' with {current_count} images. Need to add {additional_needed} more.")
        
        augmented_images_created = 0
        while augmented_images_created < additional_needed and cropped_files:
            for cropped_file in cropped_files:
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
                    if not os.path.exists(rotated_save_path):
                        rotated_img.save(rotated_save_path)
                        print(f"✅ Saved rotated {angle}° image: {rotated_save_path}")
                        augmented_images_created += 1
                        if augmented_images_created >= additional_needed:
                            break
                
                if augmented_images_created >= additional_needed:
                    break
                
                # 2. Horizontal Flip
                flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT)
                flipped_h_save_path = os.path.join(folder_path, f"{base_name}_cropped_flipH.png")
                if not os.path.exists(flipped_h_save_path):
                    flipped_h.save(flipped_h_save_path)
                    print(f"✅ Saved horizontal flip image: {flipped_h_save_path}")
                    augmented_images_created += 1
                    if augmented_images_created >= additional_needed:
                        break
                
                # 3. Vertical Flip
                flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM)
                flipped_v_save_path = os.path.join(folder_path, f"{base_name}_cropped_flipV.png")
                if not os.path.exists(flipped_v_save_path):
                    flipped_v.save(flipped_v_save_path)
                    print(f"✅ Saved vertical flip image: {flipped_v_save_path}")
                    augmented_images_created += 1
                    if augmented_images_created >= additional_needed:
                        break
                
                # 4. Optional: Combined Augmentation (Horizontal flip + 90° rotation)
                flipped_h_rotated = flipped_h.rotate(90, expand=True)
                flipped_h_rotated_save_path = os.path.join(folder_path, f"{base_name}_cropped_flipH_rot90.png")
                if not os.path.exists(flipped_h_rotated_save_path):
                    flipped_h_rotated.save(flipped_h_rotated_save_path)
                    print(f"✅ Saved horizontal flip rotated 90° image: {flipped_h_rotated_save_path}")
                    augmented_images_created += 1
                    if augmented_images_created >= additional_needed:
                        break

if __name__ == '__main__':
    dict_change, balanced = check_dataset_balance(output_path=OUTPUT_PATH)
    print(f"Missing images per category: {dict_change}")
    print(f"Is dataset balanced? {balanced}")
    
    augment_cropped_images(output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER)