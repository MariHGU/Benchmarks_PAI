import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
NUM_FOLDERS = None  # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None  # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = 'out_data/'

def check_dataset_balance(output_path=OUTPUT_PATH):
    """Checks whether each category has around 300 images.
    
    Returns:
        missing_dict (dict): Number of images needed for each PLU to reach ~300.
        is_balanced (bool): True if all categories are close to balanced, False otherwise.
    """
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
        
    # Calculate target (around 300) based on maximum count
    max_count = min(350, max(category_counts.values()))  # Target ~300-350
    
    missing_dict = {}
    is_balanced = True
    for category, count in sorted(category_counts.items()):
        missing = max(0, max_count - count)
        missing_dict[category] = missing
        if count < (max_count - 50):  # Allow some flexibility (~50 images difference)
            is_balanced = False
            
    return missing_dict, is_balanced

def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """Generates augmentations for folders with less than 300 images."""
    all_items = os.listdir(output_path)
    folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]
    
    # Limit the number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]
        
    for folder in folders:
        folder_path = os.path.join(output_path, folder)
        total_png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
        
        # Only augment if we have fewer than 300 images
        if len(total_png_files) >= 300:
            print(f"Skipping folder '{folder}' because it has {len(total_png_files)} images.")
            continue
            
        # Calculate how many more images we need
        needed = max(0, 300 - len(total_png_files))
        print(f"Need to generate {needed} more images for folder '{folder}'.")
        
        cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]
        if num_files_per_folder is not None:
            cropped_files = cropped_files[:num_files_per_folder]
            
        # Calculate how many augmentations per image we need
        augmentations_per_image = max(1, round(needed / len(cropped_files)))
        
        for idx, cropped_file in enumerate(cropped_files):
            if idx >= augmentations_per_image:
                break
                
            base_name = cropped_file.replace('_cropped.png', '')
            image_path = os.path.join(folder_path, cropped_file)
            
            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"⚠️ Failed to open image {image_path}: {e}")
                continue
                
            # Generate different augmentations
            augmentation_methods = [
                ('rot90', lambda img: img.rotate(90, expand=True)),
                ('rot180', lambda img: img.rotate(180, expand=True)),
                ('rot270', lambda img: img.rotate(270, expand=True)),
                ('flipH', lambda img: img.transpose(Image.FLIP_LEFT_RIGHT)),
                ('flipV', lambda img: img.transpose(Image.FLIP_TOP_BOTTOM)),
            ]
            
            for method_name, method in augmentation_methods:
                augmented_img = method(img)
                save_path = os.path.join(folder_path, f"{base_name}_cropped_{method_name}.png")
                augmented_img.save(save_path)
                print(f"✅ Saved {method_name} image: {save_path}")
                
def balance_dataset(output_path=OUTPUT_PATH):
    """Balances the dataset by generating augmentations where needed."""
    missing_dict, is_balanced = check_dataset_balance(output_path=output_path)
    
    if is_balanced:
        print("Dataset is already balanced with ~300 images per category.")
        return
        
    print("\nGenerating augmentations to balance the dataset...")
    augment_cropped_images(output_path=output_path, num_folders=NUM_FOLDERS, 
                          num_files_per_folder=NUM_FILES_PER_FOLDER)
    
    # Verify after augmentation
    final_missing, final_balanced = check_dataset_balance(output_path=output_path)
    if final_balanced:
        print("\nSuccessfully balanced the dataset with ~300 images per category!")
    else:
        print("\nSome categories are still unbalanced. Consider running this script again.")

if __name__ == '__main__':
    balance_dataset(output_path=OUTPUT_PATH)