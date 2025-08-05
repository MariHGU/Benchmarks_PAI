import os
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===
NUM_FOLDERS = None  # Set to None to process all folders or a specific number (e.g., 5)
NUM_FILES_PER_FOLDER = None  # Set to None to process all cropped images per folder or a specific number (e.g., 5)
OUTPUT_PATH = "out_data/"

def check_dataset_balance(output_path=OUTPUT_PATH):
    ...
    return missing_dict, is_balanced

def augment_cropped_images(missing_dict, output_path="out_data/", num_folders=None, num_files_per_folder=None):
    all_items = os.listdir(output_path)
    folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]

    # Limit the number of folders if specified
    if num_folders is not None:
        folders = folders[:num_folders]

    for folder in folders:
        folder_path = os.path.join(output_path, folder)
        total_png_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]

        # Skip augmentation if the folder already has 300 or more images
        if len(total_png_files) >= 300:
            print(f"Skipping folder '{folder}' because it already has {len(total_png_files)} images.")
            continue

        # Get all cropped images (files ending with '_cropped.png')
        cropped_files = [f for f in os.listdir(folder_path) if f.endswith("_croropped.png")]

        if num_files_per_folder is not None:
            cropped_files = cropped_files[:num_files_per_folder]

        for cropped_file in cropped_files:
            base_name = cropped_file.replace("_cropped.png", "")
            image_path = os.path.join(folder_path, cropped_file)
            plu_code = base_name.split("_")[0]  # Extract PLU code from the filename

            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"⚠️ Failed to open image {image_path}: {e}")
                continue

            # Only augment if the category (PLU code) needs more images
            if missing_dict[plu_code] > 0:
                # --- Augmentations ---
                ...

                # Update the count of missing images for the PLU code
                missing_dict[plu_code] -= 4  # Subtract the number of augmented images

        print(f"Finished processing folder: {folder}")

    print("Dataset balanced!")

if __name__ == "__main__":
    dict_change, balanced = check_dataset_balance(output_path=OUTPUT_PATH)

    if not balanced:
        augment_cropped_images(dict_change, output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER)