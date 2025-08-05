import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
TARGET_IMAGES_PER_FILE = 300
OUTPUT_PATH = 'out_data/'

def check_dataset_balance(output_path=OUTPUT_PATH):
    # ... Your existing balance checking function here ...

def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
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

        required_images = TARGET_IMAGES_PER_FILE - len(cropped_files)

        if required_images > 0:
            for _ in range(required_images):
                base_name = os.path.splitext(os.path.basename(cropped_files[-1]))[0] + '_' + str(len(cropped_files)) + '.png'
                image_path = os.path.join(folder_path, base_name)
                Image.new('RGB', (100, 100)).save(image_path)  # You can replace this with your augmentation function to create the necessary images

        # ... Your existing augmentation code here ...

if __name__ == '__main__':
    missing_dict, balanced = check_dataset_balance(output_path=OUTPUT_PATH)
    if not balanced:
        augment_cropped_images(output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER)