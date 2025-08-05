import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
NUM_FOLDERS = None  # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None  # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = 'out_data/'

def check_dataset_balance(output_path=OUTPUT_PATH, target_count=300):
    """Checks whether each category (identified by the filename prefix, assumed to be the PLU number) 
    in the output folder has the target number of images.
    
    Args:
        output_path: Path to the output directory containing images
        target_count: Target number of images per category
    
    Returns:
        missing_dict (dict): Dictionary where keys are PLU numbers and values are the number of images missing to reach the target count
        is_balanced (bool): True if every category has the target count, False otherwise
    """
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
    
    # Calculate missing images for each category
    missing_dict = {}
    is_balanced = True
    for category, count in category_counts.items():
        missing = target_count - count
        missing_dict[category] = missing
        if missing != 0:
            is_balanced = False
    
    return missing_dict, is_balanced

def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None, target_count=300):
    """Iterates over already-cropped images in the output directory and generates augmentations 
    (rotations, flips) only for categories that need more images to reach the target count.
    
    Args:
        output_path: Path to the output directory containing images
        num_folders: Limit the number of folders to process
        num_files_per_folder: Limit the number of files per folder to augment
        target_count: Target number of images per category
    """
    # Get current counts and determine missing images
    missing_dict, is_balanced = check_dataset_balance(output_path, target_count)
    
    if is_balanced:
        print("Dataset is already balanced. No need for augmentation.")
        return
    
    all_items = os.listdir(output_path)
    folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]
    
    # Limit the number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]
    
    for folder in folders:
        folder_path = os.path.join(output_path, folder)
        category = os.path.basename(folder)  # Assuming folder name matches PLU number
        
        # Get current count and calculate needed augmentations
        current_count = sum(1 for f in os.listdir(folder_path) if f.startswith(f"{category}_") and f.endswith('.png'))
        needed_augmentations = target_count - current_count
        
        if needed_augmentations <= 0:
            print(f"Skipping folder '{folder}' as it already has enough images.")
            continue
        
        print(f"Processing folder '{folder}': Need {needed_augmentations} more images")
        
        # Get all cropped images
        cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]
        
        # Limit the number of files per folder if specified
        if num_files_per_folder is not None:
            cropped_files = cropped_files[:num_files_per_folder]
        
        # Augment each cropped image until we reach target_count
        for cropped_file in cropped_files:
            base_name = os.path.splitext(cropped_file)[0].replace('_cropped', '')
            
            image_path = os.path.join(folder_path, cropped_file)
            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"⚠️ Failed to open image {image_path}: {e}")
                continue
            
            # Generate augmentations
            current_count += 1  # Count this new augmented image
            if current_count >= target_count:
                break
            
            # Generate different versions of the image
            for angle in [90, 180, 270]:
                rotated_img = img.rotate(angle)
                rotated_filename = f"{base_name}_rot{angle}.png"
                rotated_path = os.path.join(folder_path, rotated_filename)
                if not os.path.exists(rotated_path):  # Avoid overwriting existing files
                    rotated_img.save(rotated_path)
                    print(f"✅ Saved rotated {angle}° image: {rotated_path}")
                    current_count +=1
                    if current_count >= target_count:
                        break
            
            # Flip images
            flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT)
            flipped_h_filename = f"{base_name}_flipH.png"
            flipped_h_path = os.path.join(folder_path, flipped_h_filename)
            if not os.path.exists(flipped_h_path):
                flipped_h.save(flipped_h_path)
                print(f"✅ Saved horizontal flip image: {flipped_h_path}")
                current_count +=1
            
            flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM)
            flipped_v_filename = f"{base_name}_flipV.png"
            flipped_v_path = os.path.join(folder_path, flipped_v_filename)
            if not os.path.exists(flipped_v_path):
                flipped_v.save(flipped_v_path)
                print(f"✅ Saved vertical flip image: {flipped_v_path}")
                current_count +=1
            
            # Combined augmentation (flip + rotate)
            flipped_h_rot90 = flipped_h.transpose(Image.ROTATE_90)
            flipped_h_rot90_filename = f"{base_name}_flipH_rot90.png"
            flipped_h_rot90_path = os.path.join(folder_path, flipped_h_rot90_filename)
            if not os.path.exists(flipped_h_rot90_path):
                flipped_h_rot90.save(flipped_h_rot90_path)
                print(f"✅ Saved horizontal flip + 90° rotation image: {flipped_h_rot90_path}")
                current_count +=1

if __name__ == '__main__':
    # Example usage
    augment_cropped_images(output_path=OUTPUT_PATH, num_folders=None, num_files_per_folder=None)