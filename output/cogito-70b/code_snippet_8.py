import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
TARGET_COUNT = 300  # Target number of images per category
NUM_FOLDERS = None  # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None  # Set to None to process all cropped images per folder

def check_dataset_balance(output_path='out_data/'):
    """Checks whether each category in the output folder has the target count of images.
    
    Returns:
        missing_dict (dict): A dictionary where keys are PLU numbers and values are 
                            the number of images missing to reach the target count.
        is_balanced (bool): True if every category has at least the target count, False otherwise.
    """
    all_files = [f for f in os.listdir(output_path) if f.endswith('.png')]
    
    # Count images per category
    category_counts = defaultdict(int)
    for filename in all_files:
        parts = filename.split('_')
        if len(parts) > 1:
            category = parts[0]
            category_counts[category] += 1
    
    if not category_counts:
        print("No images found in the output folder.")
        return {}, True
    
    # Build a dictionary of missing images per category
    missing_dict = {}
    is_balanced = True
    for category, count in sorted(category_counts.items()):
        missing = max(0, TARGET_COUNT - count)
        missing_dict[category] = missing
        if missing > 0:
            is_balanced = False
            
    return missing_dict, is_balanced

def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """Generates augmented images for categories that need more pictures to reach the target count."""
    
    # First check which categories need augmentation
    missing_dict, is_balanced = check_dataset_balance(output_path)
    
    if is_balanced:
        print("Dataset is already balanced. No augmentation needed.")
        return
    
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
            
        for cropped_file in cropped_files:
            base_name = cropped_file.replace('_cropped.png', '')
            image_path = os.path.join(folder_path, cropped_file)
            
            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"⚠️ Failed to open image {image_path}: {e}")
                continue
            
            # Check if this category needs more images
            category = base_name.split('_')[0]
            if missing_dict[category] <= 0:
                continue
                
            # Generate augmentations until we reach the target count
            while missing_dict[category] > 0:
                augmentation_suffix = f"_aug{missing_dict[category]}"
                augmented_path = os.path.join(folder_path, f"{base_name}{augmentation_suffix}.png")
                
                # Simple augmentation: rotate by a random angle and flip horizontally/vertically
                import random
                angle = random.randint(10, 350)
                img_rotated = img.rotate(angle, expand=True)
                
                if random.random() < 0.5:
                    img_rotated = img_rotated.transpose(Image.FLIP_LEFT_RIGHT)
                if random.random() < 0.5:
                    img_rotated = img_rotated.transpose(Image.FLIP_TOP_BOTTOM)
                    
                try:
                    img_rotated.save(augmented_path)
                    missing_dict[category] -= 1
                    print(f"✅ Saved augmented image: {augmented_path}")
                except Exception as e:
                    print(f"⚠️ Failed to save image {augmented_path}: {e}")
                    continue

if __name__ == '__main__':
    augment_cropped_images(output_path='out_data/', 
                           num_folders=NUM_FOLDERS, 
                           num_files_per_folder=NUM_FILES_PER_FOLDER)