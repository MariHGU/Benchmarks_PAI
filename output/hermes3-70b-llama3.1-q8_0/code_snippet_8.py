import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
NUM_FOLDERS = None  # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None  # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = 'out_data/'

def check_dataset_balance(output_path=OUTPUT_PATH):
    """
    Checks whether each category (identified by the filename prefix, assumed to be the PLU number) in the output folder has the same number of images as the category with the highest count.
    
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
        missing = 300 - count
        missing_dict[category] = missing
        if missing > 0:
            is_balanced = False
    
    return missing_dict, is_balanced

def augment_cropped_images(missing_dict, output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """
    Iterates over already-cropped images in the output directory and generates augmentations (rotations, horizontal flip, vertical flip, and a combined flip + rotation)
    only if the folder has less than 300 PNG images.
    """
    all_items = os.listdir(output_path)
    folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]
    
    # Limit the number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]
    
    for folder in folders:
        folder_path = os.path.join(output_path, folder)
        
        # Count total PNG files in the folder
        total_png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
        if len(total_png_files) >= 300:
            print(f"Skipping folder '{folder}' because it already has {len(total_png_files)} images.")
            continue
        
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
            
            # 3. Vertical Flip
            flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM)
            flipped_v_save_path = os.path.join(folder_path, f"{base_name}_cropped_flipV.png")
            flipped_v.save(flipped_v_save_path)
            print(f"✅ Saved vertical flip image: {flipped_v_save_path}")
            
            # 4. Optional: Combined Augmentation (Horizontal flip + 90° rotation)
            flipped_h_rotated = flipped_h.rotate(90, expand=True)
            flipped_h_rotated_save_path = os.path.join(folder_path, f"{base_name}_cropped_flipH_rot90.png")
            flipped_h_rotated.save(flipped_h_rotated_save_path)
            print(f"✅ Saved horizontal flip rotated 90° image: {flipped_h_rotated_save_path}")

if __name__ == '__main__':
    missing_dict, balanced = check_dataset_balance(output_path=OUTPUT_PATH)
    if not balanced:
        augment_cropped_images(missing_dict, output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER)