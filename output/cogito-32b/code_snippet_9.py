import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
NUM_FOLDERS = None  # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None  # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = 'out_data/'
TARGET_COUNT = 300

def check_dataset_balance(output_path=OUTPUT_PATH):
    """Checks whether each category in the output folder and returns how many images are needed for balance."""
    # List all PNG files in the output folder
    all_files = [f for f in os.listdir(output_path) if f.endswith('.png')]
    
    # Count images per category
    category_counts = defaultdict(int)
    for filename in all_files:
        parts = filename.split('_')
        if parts:
            category = parts[0]
            category_counts[category] += 1
    
    if not category_counts:
        print("No images found in the output folder.")
        return {}, True
    
    # Build a dictionary of missing images per category to reach target count
    missing_dict = {}
    for category, count in sorted(category_counts.items()):
        missing = max(0, TARGET_COUNT - count)
        missing_dict[category] = missing
    
    is_balanced = all(count >= TARGET_COUNT for count in category_counts.values())
    return missing_dict, is_balanced

def augment_cropped_images(output_path='out_data/', num_folders=None):
    """Generates augmentations for folders that need more images to reach the target count."""
    all_items = os.listdir(output_path)
    folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]
    
    # Limit the number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]
    
    missing_dict, _ = check_dataset_balance(output_path)
    
    for folder in folders:
        folder_path = os.path.join(output_path, folder)
        
        # Skip if this category already has enough images
        if missing_dict.get(folder.split('_')[0], 0) == 0:
            continue
        
        # Get all cropped images (files ending with '_cropped.png')
        cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]
        
        current_count = len([f for f in os.listdir(folder_path) if f.endswith('.png')])
        needed_images = missing_dict[folder.split('_')[0]]
        
        if current_count >= TARGET_COUNT:
            print(f"Skipping folder '{folder}' because it already has {current_count} images.")
            continue
        
        # Calculate how many augmentations to generate for each image
        augment_per_image = max(1, needed_images // len(cropped_files))
        
        for cropped_file in cropped_files:
            base_name = cropped_file.replace('_cropped.png', '')
            image_path = os.path.join(folder_path, cropped_file)
            
            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"⚠️ Failed to open image {image_path}: {e}")
                continue
            
            # Generate augmentations
            for _ in range(augment_per_image):
                # 1. Rotations (90°, 180°, 270°)
                for angle in [90, 180, 270]:
                    rotated_img = img.rotate(angle, expand=True)
                    rotated_save_path = os.path.join(folder_path, f"{base_name}_cropped_rot{angle}_{needed_images}.png")
                    rotated_img.save(rotated_save_path)
                
                # 2. Horizontal Flip
                flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT)
                flipped_h_save_path = os.path.join(folder_path, f"{base_name}_cropped_flipH_{needed_images}.png")
                flipped_h.save(flipped_h_save_path)
                
                # 3. Vertical Flip
                flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM)
                flipped_v_save_path = os.path.join(folder_path, f"{base_name}_cropped_flipV_{needed_images}.png")
                flipped_v.save(flipped_v_save_path)

def main():
    missing_dict, is_balanced = check_dataset_balance(OUTPUT_PATH)
    
    if not is_balanced:
        print(f"Dataset needs balancing. Missing images per category: {missing_dict}")
        augment_cropped_images(output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS)
    else:
        print("Dataset is already balanced.")

if __name__ == '__main__':
    main()