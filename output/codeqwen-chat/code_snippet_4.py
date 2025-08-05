import os
from PIL import Image
from collections import defaultdict

# ... (previous code remains unchanged)

def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """
    Iterates over already-cropped images in the output directory and generates augmentations 
    (rotations, horizontal flip, vertical flip, and a combined flip + rotation) only if the 
    folder has less than 200 PNG images.
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
        if len(total_png_files) >= 200:
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

            # Check if the category count exceeds 300 after each augmentation
            category = folder.split('_')[0]  # Assuming the category is the first part of the filename before an underscore
            total_png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
            if len(total_png_files) >= 300:
                print(f"Breaking out of folder '{folder}' because it has more than {len(total_png_files)} images.")
                break

# ... (previous code remains unchanged)