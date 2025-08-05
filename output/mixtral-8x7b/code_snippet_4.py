def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """
    Iterates over already-cropped images in the output directory and generates augmentations (rotations, horizontal flip, vertical flip, and a combined flip + rotation) only if the folder has less than 300 PNG images.
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
        
        # Check if the folder needs augmentation
        target_count = 300
        num_additional_images_needed = max(0, target_count - len(total_png_files))

        if num_additional_images_needed == 0:
            print(f"Skipping folder '{folder}' because it already has {len(total_png_files)} images.")
            continue
        
        cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]

        # Limit the number of files per folder if specified
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
            # ... (The rest of the augmentation code)
            
            num_additional_images_generated = 0

            for _ in range(num_additional_images_needed):
                # Generate and save an augmented image
                augmented_img, saved_filename = generate_and_save_augmented_image(img, folder_path, base_name)
                num_additional_images_generated += 1

            print(f"✅ Generated {num_additional_images_generated} additional augmentations for file '{base_name}' in folder '{folder}', now at {len(os.listdir(folder_path))} images.")