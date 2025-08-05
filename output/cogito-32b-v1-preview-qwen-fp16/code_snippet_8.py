import os
from PIL import Image
from collections import defaultdict
import random

# === CONFIGURATION ===
NUM_FOLDERS = None      # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None   # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = 'out_data/'
TARGET_COUNT = 300     # Target number of images per category

def check_dataset_balance(output_path=OUTPUT_PATH):
    """Checks whether each category has reached the target count.
    
    Returns:
        missing_dict (dict): A dictionary where keys are PLU numbers and values 
                            are the number of images still needed to reach TARGET_COUNT.
        is_balanced (bool): True if every category has at least TARGET_COUNT, False otherwise.
    """
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

    # Calculate missing images per category
    missing_dict = {}
    is_balanced = all(count >= TARGET_COUNT for count in category_counts.values())
    
    for category, count in sorted(category_counts.items()):
        missing = max(0, TARGET_COUNT - count)
        missing_dict[category] = missing
    
    return missing_dict, is_balanced

def augment_cropped_images(output_path='out_data/', num_folders=None):
    """Generates augmented images until each folder reaches the target count."""
    
    folders = [f for f in sorted(os.listdir(output_path)) 
              if os.path.isdir(os.path.join(output_path, f))]
    
    # Limit number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]
    
    while True:  # Continue until all folders reach target count
        missing_dict, balanced = check_dataset_balance(output_path)
        
        if balanced:
            print("Dataset has been successfully balanced!")
            break
        
        for folder in folders:
            folder_path = os.path.join(output_path, folder)
            
            # Check current count and number of images needed
            current_count = len([f for f in os.listdir(folder_path) if f.endswith('.png')])
            missing_images = max(0, TARGET_COUNT - current_count)
            
            if missing_images <= 0:
                continue
            
            print(f"Folder '{folder}' needs {missing_images} more images.")
            
            # Get all cropped images
            cropped_files = [f for f in os.listdir(folder_path) 
                           if f.endswith('_cropped.png')]
            
            if not cropped_files:
                print(f"No cropped images found in folder '{folder}'. Skipping...")
                continue
            
            # Select a random image to augment
            selected_image = random.choice(cropped_files)
            base_name = selected_image.replace('_cropped.png', '')
            image_path = os.path.join(folder_path, selected_image)
            
            try:
                img = Image.open(image_path)
                
                # Generate augmented images until we reach target count
                while current_count < TARGET_COUNT and missing_images > 0:
                    augmentation_type = random.choice(['rotate', 'flip_h', 'flip_v'])
                    
                    if augmentation_type == 'rotate':
                        angle = random.choice([90, 180, 270])
                        augmented_img = img.rotate(angle, expand=True)
                        save_path = os.path.join(folder_path, 
                                               f"{base_name}_cropped_rot{angle}.png")
                    elif augmentation_type == 'flip_h':
                        augmented_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                        save_path = os.path.join(folder_path, 
                                               f"{base_name}_cropped_flipH.png")
                    else:  # flip_v
                        augmented_img = img.transpose(Image.FLIP_TOP_BOTTOM)
                        save_path = os.path.join(folder_path, 
                                               f"{base_name}_cropped_flipV.png")
                    
                    augmented_img.save(save_path)
                    current_count += 1
                    missing_images -= 1
                    
                    print(f"Generated {augmentation_type} augmentation: {save_path}")
                
                img.close()
            
            except Exception as e:
                print(f"⚠️ Failed to process image {image_path}: {e}")
        
        # Check balance again after one iteration of augmenting
        missing_dict, balanced = check_dataset_balance(output_path)
    
    return True

if __name__ == '__main__':
    dict_change, balanced = check_dataset_balance(output_path=OUTPUT_PATH)
    
    if not balanced:
        print(f"Dataset is unbalanced. Starting augmentation to reach {TARGET_COUNT} images per category.")
        augment_cropped_images(output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS)